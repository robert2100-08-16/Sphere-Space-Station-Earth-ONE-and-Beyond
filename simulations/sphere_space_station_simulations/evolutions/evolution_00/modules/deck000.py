"""
EVOL-00 – DECK000 "Wormhole" baseline CAD geometry (SemVer v0.1.1).

This revision integrates rectangular window apertures and placeholder glazing
panels into the window-tube segments per the EVOL‑00 specification.

Generates a segmented axial tube with:
 - Overall length: 127 m
 - Barrel: OD 22 m, ID 20 m
 - Six docking-ring modules: 10 m axial length, ID 20 m (constricted throat), OD flush (22 m)
 - Start of first ring at 3.5 m from the North pole interior face
 - Ring pitch 20 m; window-tube modules (10 m) between rings
 - 3.5 m service clearances at both ends

Exports:
 - OBJ mesh (watertight shell segments per module)
 - CSV segment table (Table 1 equivalent)
 - glTF binary with basic materials

Note:
CadQuery could generate these solids parametrically and offer richer
modelling capabilities, but its heavy dependency footprint keeps this
evolution on a lightweight, hand-rolled mesh builder for now.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple
import math
import csv
import numpy as np
from pygltflib import (
    GLTF2,
    Scene,
    Node,
    Mesh as GLTFMesh,
    Buffer,
    BufferView,
    Accessor,
    Primitive,
    PbrMetallicRoughness,
    Material as GLTFMaterial,
)

from simulations.sphere_space_station_simulations.data_model import (
    ALUMINIUM,
    GLASS,
    Material,
    STEEL,
)

# -------------------------
# Parameters & segment plan
# -------------------------


@dataclass(frozen=True)
class Deck000Params:
    length: float = 127.0
    barrel_od: float = 22.0
    barrel_id: float = 20.0
    ring_id: float = 20.0
    ring_len: float = 10.0
    window_len: float = 10.0
    ring_first_offset: float = 3.5
    ring_pitch: float = 20.0
    n_rings: int = 6  # 00..05
    end_clearance: float = 3.5
    radial_segments: int = 96  # circle tessellation
    ring_material: Material = field(default_factory=lambda: STEEL)
    window_material: Material = field(default_factory=lambda: ALUMINIUM)
    clearance_material: Material = field(default_factory=lambda: ALUMINIUM)
    windows_per_segment: int = 8
    window_width: float = 4.0
    window_height: float = 3.0
    glass_material: Material = field(default_factory=lambda: GLASS)

    @property
    def barrel_ro(self) -> float:
        return self.barrel_od * 0.5

    @property
    def barrel_ri(self) -> float:
        return self.barrel_id * 0.5

    @property
    def ring_ri(self) -> float:
        return self.ring_id * 0.5


def generate_segments(p: Deck000Params) -> List[Dict]:
    """
    Generate Table-1-like segment list from North (z=0) to South (z=length).
    Segment types: 'clearance', 'ring', 'window'
    """
    segments: List[Dict] = []

    # North clearance
    z = 0.0
    if p.end_clearance > 0:
        segments.append(
            dict(
                name="clearance_north",
                type="clearance",
                z0=0.0,
                z1=p.end_clearance,
                r_inner=p.barrel_ri,
                r_outer=p.barrel_ro,
                note="forward clearance / taper / systems",
                material=p.clearance_material,
            )
        )
        z = p.end_clearance

    # Alternating ring / window modules
    for i in range(p.n_rings):
        # Position of ring i
        ring_z0 = p.ring_first_offset + i * p.ring_pitch
        ring_z1 = ring_z0 + p.ring_len
        # Window before/after depending on sequence:
        # The baseline has a 10 m 'window tube' between rings.
        # We add the window segment that precedes the next ring (except before the very first ring).
        if i == 0:
            # Immediately add the first ring (3.5..13.5)
            segments.append(
                dict(
                    name=f"ring_{i:02d}",
                    type="ring",
                    z0=ring_z0,
                    z1=ring_z1,
                    r_inner=p.ring_ri,
                    r_outer=p.barrel_ro,
                    note="Inconel ring, constricted ID",
                    material=p.ring_material,
                )
            )
        else:
            # Window segment from end of previous ring to start of this ring
            prev_ring_z1 = p.ring_first_offset + (i - 1) * p.ring_pitch + p.ring_len
            segments.append(
                dict(
                    name=f"window_{i-1:02d}",
                    type="window",
                    z0=prev_ring_z1,
                    z1=ring_z0,
                    r_inner=p.barrel_ri,
                    r_outer=p.barrel_ro,
                    note="window tube (apertures to be detailed in EV1)",
                    material=p.window_material,
                )
            )
            # This ring
            segments.append(
                dict(
                    name=f"ring_{i:02d}",
                    type="ring",
                    z0=ring_z0,
                    z1=ring_z1,
                    r_inner=p.ring_ri,
                    r_outer=p.barrel_ro,
                    note="Inconel ring, constricted ID",
                    material=p.ring_material,
                )
            )

    # Window after last ring up to (length - clearance)
    last_ring_z1 = p.ring_first_offset + (p.n_rings - 1) * p.ring_pitch + p.ring_len
    tail_z1 = p.length - p.end_clearance
    if tail_z1 > last_ring_z1:
        segments.append(
            dict(
                name=f"window_{p.n_rings:02d}",
                type="window",
                z0=last_ring_z1,
                z1=tail_z1,
                r_inner=p.barrel_ri,
                r_outer=p.barrel_ro,
                note="window tube (apertures to be detailed in EV1)",
                material=p.window_material,
            )
        )

    # South clearance
    if p.end_clearance > 0:
        segments.append(
            dict(
                name="clearance_south",
                type="clearance",
                z0=tail_z1,
                z1=p.length,
                r_inner=p.barrel_ri,
                r_outer=p.barrel_ro,
                note="aft clearance / taper / systems",
                material=p.clearance_material,
            )
        )

    return segments


# -------------------------
# Simple mesh primitives
# -------------------------


class Mesh:
    __slots__ = ("name", "vertices", "faces", "material")

    def __init__(self, name: str, material: Material):
        self.name = name
        self.material = material
        self.vertices: List[Tuple[float, float, float]] = []
        self.faces: List[Tuple[int, int, int]] = []

    def merge(self, other: "Mesh") -> None:
        offset = len(self.vertices)
        self.vertices.extend(other.vertices)
        self.faces.extend(
            [(a + offset, b + offset, c + offset) for (a, b, c) in other.faces]
        )


def tube_segment(
    name: str,
    z0: float,
    z1: float,
    r_inner: float,
    r_outer: float,
    radial_segments: int,
    material: Material,
) -> Mesh:
    """
    Create a hollow cylindrical shell between z0 and z1.
    - Outer and inner skins (no end caps for contiguous assembly)
    """
    m = Mesh(name, material)
    n = radial_segments
    two_pi = 2.0 * math.pi

    # Outer ring vertices at z0 and z1
    vo0 = []
    vo1 = []
    for i in range(n):
        a = two_pi * i / n
        x = r_outer * math.cos(a)
        y = r_outer * math.sin(a)
        vo0.append(len(m.vertices))
        m.vertices.append((x, y, z0))
        vo1.append(len(m.vertices))
        m.vertices.append((x, y, z1))

    # Inner ring vertices at z0 and z1 (clockwise reversed to keep outward normals outward-ish)
    vi0 = []
    vi1 = []
    for i in range(n):
        a = two_pi * i / n
        x = r_inner * math.cos(a)
        y = r_inner * math.sin(a)
        vi0.append(len(m.vertices))
        m.vertices.append((x, y, z0))
        vi1.append(len(m.vertices))
        m.vertices.append((x, y, z1))

    # Quads -> triangles for outer skin
    for i in range(n):
        i_next = (i + 1) % n
        a0 = vo0[i]
        b0 = vo0[i_next]
        a1 = vo1[i]
        b1 = vo1[i_next]
        # two triangles (a0, a1, b1) and (a0, b1, b0)
        m.faces.append((a0, a1, b1))
        m.faces.append((a0, b1, b0))

    # Quads -> triangles for inner skin (flip winding)
    for i in range(n):
        i_next = (i + 1) % n
        a0 = vi0[i]
        b0 = vi0[i_next]
        a1 = vi1[i]
        b1 = vi1[i_next]
        # flip winding to face inward (so normals 'inward' -> okay for CAD viewers)
        m.faces.append((a0, b1, a1))
        m.faces.append((a0, b0, b1))

    return m


def window_panel(
    name: str,
    angle: float,
    z0: float,
    z1: float,
    r_inner: float,
    r_outer: float,
    height: float,
    material: Material,
) -> Mesh:
    """Create a simple rectangular prism representing a window pane."""
    m = Mesh(name, material)
    thickness = r_outer - r_inner
    half_w = (z1 - z0) * 0.5
    half_h = height * 0.5
    center_z = (z0 + z1) * 0.5
    radius_mid = (r_inner + r_outer) * 0.5
    nx = math.cos(angle)
    ny = math.sin(angle)
    tx = -math.sin(angle)
    ty = math.cos(angle)

    # Create 8 vertices of the box
    for dx in (-thickness * 0.5, thickness * 0.5):
        for dy in (-half_h, half_h):
            for dz in (-half_w, half_w):
                x = (radius_mid + dx) * nx + dy * tx
                y = (radius_mid + dx) * ny + dy * ty
                z = center_z + dz
                m.vertices.append((x, y, z))

    # Six faces
    faces = [
        (0, 2, 3, 1),
        (4, 5, 7, 6),
        (0, 1, 5, 4),
        (2, 6, 7, 3),
        (1, 3, 7, 5),
        (0, 4, 6, 2),
    ]
    for a, b, c, d in faces:
        m.faces.append((a, b, c))
        m.faces.append((a, c, d))
    return m


def tube_segment_with_windows(
    name: str,
    z0: float,
    z1: float,
    r_inner: float,
    r_outer: float,
    radial_segments: int,
    material: Material,
    windows_per_segment: int,
    window_width: float,
    window_height: float,
    glass_material: Material,
) -> List[Mesh]:
    """Create a tube segment and cut rectangular window apertures."""
    meshes: List[Mesh] = []
    # Angles for window centres
    angle_step = 2.0 * math.pi / windows_per_segment
    half_angle = (window_height / r_outer) * 0.5
    window_angles = [i * angle_step for i in range(windows_per_segment)]

    # z ranges
    center_z = (z0 + z1) * 0.5
    win_z0 = center_z - window_width * 0.5
    win_z1 = center_z + window_width * 0.5

    # Build tube with additional z-rings for window span
    m = Mesh(name, material)
    zs = [z0, win_z0, win_z1, z1]
    n = radial_segments
    two_pi = 2.0 * math.pi
    angles = [two_pi * i / n for i in range(n)]

    vo: List[List[int]] = []
    vi: List[List[int]] = []
    for z in zs:
        vo_ring = []
        vi_ring = []
        for a in angles:
            x = r_outer * math.cos(a)
            y = r_outer * math.sin(a)
            vo_ring.append(len(m.vertices))
            m.vertices.append((x, y, z))
            x = r_inner * math.cos(a)
            y = r_inner * math.sin(a)
            vi_ring.append(len(m.vertices))
            m.vertices.append((x, y, z))
        vo.append(vo_ring)
        vi.append(vi_ring)

    def angle_in_window(a: float) -> bool:
        for c in window_angles:
            if abs((a - c + math.pi) % (2 * math.pi) - math.pi) <= half_angle:
                return True
        return False

    # Outer and inner skins except window span
    for k in range(len(zs) - 1):
        for i, a in enumerate(angles):
            i_next = (i + 1) % n
            if k == 1 and (angle_in_window(a) or angle_in_window(angles[i_next])):
                continue
            a0 = vo[k][i]
            b0 = vo[k][i_next]
            a1 = vo[k + 1][i]
            b1 = vo[k + 1][i_next]
            m.faces.append((a0, a1, b1))
            m.faces.append((a0, b1, b0))
            a0 = vi[k][i]
            b0 = vi[k][i_next]
            a1 = vi[k + 1][i]
            b1 = vi[k + 1][i_next]
            m.faces.append((a0, b1, a1))
            m.faces.append((a0, b0, b1))

    meshes.append(m)

    # Add glass panels
    for j, c in enumerate(window_angles):
        meshes.append(
            window_panel(
                name=f"window-pane-{name}-{j:02d}",
                angle=c,
                z0=win_z0,
                z1=win_z1,
                r_inner=r_inner,
                r_outer=r_outer,
                height=window_height,
                material=glass_material,
            )
        )
    return meshes


def build_meshes_for_segments(segments: List[Dict], p: Deck000Params) -> List[Mesh]:
    meshes: List[Mesh] = []
    for seg in segments:
        name = f"{seg['type']}-{seg['name']}"
        if seg["type"] == "window":
            meshes.extend(
                tube_segment_with_windows(
                    name=name,
                    z0=seg["z0"],
                    z1=seg["z1"],
                    r_inner=seg["r_inner"],
                    r_outer=seg["r_outer"],
                    radial_segments=p.radial_segments,
                    material=seg["material"],
                    windows_per_segment=p.windows_per_segment,
                    window_width=p.window_width,
                    window_height=p.window_height,
                    glass_material=p.glass_material,
                )
            )
        else:
            meshes.append(
                tube_segment(
                    name=name,
                    z0=seg["z0"],
                    z1=seg["z1"],
                    r_inner=seg["r_inner"],
                    r_outer=seg["r_outer"],
                    radial_segments=p.radial_segments,
                    material=seg["material"],
                )
            )
    return meshes


# -------------------------
# Exports (OBJ + CSV)
# -------------------------


def export_obj(meshes: List[Mesh], out_path: Path) -> None:
    """
    Write a single OBJ containing all meshes as named objects.
    No MTL, no normals/UVs (CAD-friendly lightweight mesh).
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write("# DECK000 EVOLUTION 0 – generated OBJ\n")
        vert_offset = 1
        for m in meshes:
            f.write(f"o {m.name}\n")
            for x, y, z in m.vertices:
                f.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
            for a, b, c in m.faces:
                f.write(f"f {a+vert_offset} {b+vert_offset} {c+vert_offset}\n")
            vert_offset += len(m.vertices)


def export_csv(segments: List[Dict], out_csv: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "Segment",
                "Type",
                "Axial start (m)",
                "Axial end (m)",
                "Axial length (m)",
                "r_inner (m)",
                "r_outer (m)",
                "Material",
                "Notes",
            ]
        )
        for seg in segments:
            w.writerow(
                [
                    seg["name"],
                    seg["type"],
                    f"{seg['z0']:.3f}",
                    f"{seg['z1']:.3f}",
                    f"{(seg['z1']-seg['z0']):.3f}",
                    f"{seg['r_inner']:.3f}",
                    f"{seg['r_outer']:.3f}",
                    seg["material"].name,
                    seg.get("note", ""),
                ]
            )


def export_gltf(meshes: List[Mesh], out_path: Path) -> None:
    """Export meshes to a binary glTF (.glb) file."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    gltf = GLTF2()
    gltf.scenes = [Scene(nodes=list(range(len(meshes))))]
    gltf.nodes = []
    gltf.meshes = []
    gltf.bufferViews = []
    gltf.accessors = []
    gltf.materials = []
    material_lookup: Dict[str, int] = {}
    binary = bytearray()

    def _ensure_material(mat: Material) -> int:
        if mat.name not in material_lookup:
            color = list(mat.color_rgba) if mat.color_rgba else [0.8, 0.8, 0.8, 1.0]
            gltf.materials.append(
                GLTFMaterial(
                    name=mat.name,
                    pbrMetallicRoughness=PbrMetallicRoughness(
                        baseColorFactor=color,
                        metallicFactor=0.8,
                        roughnessFactor=0.4,
                    ),
                )
            )
            material_lookup[mat.name] = len(gltf.materials) - 1
        return material_lookup[mat.name]

    for mesh in meshes:
        verts = np.array(mesh.vertices, dtype=np.float32)
        faces = np.array(mesh.faces, dtype=np.uint32)
        idx = faces.flatten()

        v_offset = len(binary)
        binary.extend(verts.tobytes())
        gltf.bufferViews.append(
            BufferView(
                buffer=0,
                byteOffset=v_offset,
                byteLength=verts.nbytes,
                target=34962,
            )
        )
        gltf.accessors.append(
            Accessor(
                bufferView=len(gltf.bufferViews) - 1,
                componentType=5126,
                count=len(verts),
                type="VEC3",
                min=[float(x) for x in verts.min(axis=0)],
                max=[float(x) for x in verts.max(axis=0)],
            )
        )

        i_offset = len(binary)
        binary.extend(idx.tobytes())
        gltf.bufferViews.append(
            BufferView(
                buffer=0,
                byteOffset=i_offset,
                byteLength=idx.nbytes,
                target=34963,
            )
        )
        gltf.accessors.append(
            Accessor(
                bufferView=len(gltf.bufferViews) - 1,
                componentType=5125,
                count=len(idx),
                type="SCALAR",
                min=[int(idx.min())],
                max=[int(idx.max())],
            )
        )

        mat_index = _ensure_material(mesh.material)
        gltf.meshes.append(
            GLTFMesh(
                primitives=[
                    Primitive(
                        attributes={"POSITION": len(gltf.accessors) - 2},
                        indices=len(gltf.accessors) - 1,
                        material=mat_index,
                    )
                ],
                name=mesh.name,
            )
        )
        gltf.nodes.append(Node(mesh=len(gltf.meshes) - 1, name=mesh.name))

    gltf.buffers = [Buffer(byteLength=len(binary))]
    gltf.set_binary_blob(binary)
    gltf.save_binary(str(out_path))


# -------------------------
# High-level build entry
# -------------------------


def build_and_export_ev0(
    out_dir: Path | str = "simulations/results/evolutions/evolution-00",
) -> Dict[str, Path]:
    """
    Generates EV0 geometry & reports into out_dir.
    Returns dict with key artifacts.
    """
    try:
        print(f"Building EV0 artifacts in {out_dir}...")
        if isinstance(out_dir, str):
            # Ensure out_dir is a Path object
            out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        p = Deck000Params()
        segments = generate_segments(p)
        meshes = build_meshes_for_segments(segments, p)

        obj_path = out_dir / "deck000_ev0.obj"
        csv_path = out_dir / "deck000_ev0_segments.csv"
        gltf_path = out_dir / "deck000_ev0.glb"

        # Ensure each export operation is wrapped in try-except
        try:
            export_obj(meshes, obj_path)
        except Exception as e:
            print(f"Error exporting OBJ: {e}")
            raise

        try:
            export_csv(segments, csv_path)
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            raise

        try:
            export_gltf(meshes, gltf_path)
        except Exception as e:
            print(f"Error exporting GLTF: {e}")
            raise

        return {"obj": obj_path, "csv": csv_path, "gltf": gltf_path}

    except Exception as e:
        print(f"Error in build_and_export_ev0: {e}")
        raise


if __name__ == "__main__":
    artifacts = build_and_export_ev0()
    print("EVOLUTION 00 generated:")
    for k, v in artifacts.items():
        print(f" - {k}: {v}")
