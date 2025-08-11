"""
EVOL-00 – DECK000 "Wormhole" baseline CAD geometry (SemVer v0.1.0).

This initial version models the axial tube **without** window apertures to keep
meshing robust.  According to the SSOT, EVOL‑00 includes rectangular window
units between the docking rings; those cut-outs will follow in v0.1.1.

Generates a segmented axial tube with:
 - Overall length: 127 m
 - Barrel: OD 22 m, ID 20 m
 - Six docking-ring modules: 10 m axial length, ID 10 m (constricted throat), OD flush (22 m)
 - Start of first ring at 3.5 m from the North pole interior face
 - Ring pitch 20 m; window-tube modules (10 m) between rings
 - 3.5 m service clearances at both ends

Exports:
 - OBJ mesh (watertight shell segments per module)
 - CSV segment table (Table 1 equivalent)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict
import math
import csv

# -------------------------
# Parameters & segment plan
# -------------------------


@dataclass(frozen=True)
class Deck000Params:
    length: float = 127.0
    barrel_od: float = 22.0
    barrel_id: float = 20.0
    ring_id: float = 10.0
    ring_len: float = 10.0
    window_len: float = 10.0
    ring_first_offset: float = 3.5
    ring_pitch: float = 20.0
    n_rings: int = 6  # 00..05
    end_clearance: float = 3.5
    radial_segments: int = 96  # circle tessellation

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
            )
        )

    return segments


# -------------------------
# Simple mesh primitives
# -------------------------


class Mesh:
    __slots__ = ("name", "vertices", "faces")

    def __init__(self, name: str):
        self.name = name
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
) -> Mesh:
    """
    Create a hollow cylindrical shell between z0 and z1.
    - Outer and inner skins (no end caps for contiguous assembly)
    """
    m = Mesh(name)
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


def build_meshes_for_segments(segments: List[Dict], p: Deck000Params) -> List[Mesh]:
    meshes: List[Mesh] = []
    for seg in segments:
        name = f"{seg['type']}-{seg['name']}"
        meshes.append(
            tube_segment(
                name=name,
                z0=seg["z0"],
                z1=seg["z1"],
                r_inner=seg["r_inner"],
                r_outer=seg["r_outer"],
                radial_segments=p.radial_segments,
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
                    seg.get("note", ""),
                ]
            )


# -------------------------
# High-level build entry
# -------------------------


def build_and_export_ev0(
    out_dir: Path | str = "simulations/results/deck000_evo0",
) -> Dict[str, Path]:
    """
    Generates EV0 geometry & reports into out_dir.
    Returns dict with key artifacts.
    """
    out_dir = Path(out_dir)
    p = Deck000Params()
    segments = generate_segments(p)
    meshes = build_meshes_for_segments(segments, p)

    obj_path = out_dir / "deck000_ev0.obj"
    csv_path = out_dir / "deck000_ev0_segments.csv"

    export_obj(meshes, obj_path)
    export_csv(segments, csv_path)

    return {"obj": obj_path, "csv": csv_path}


if __name__ == "__main__":
    artifacts = build_and_export_ev0()
    print("EVOLUTION 0 generated:")
    for k, v in artifacts.items():
        print(f" - {k}: {v}")
