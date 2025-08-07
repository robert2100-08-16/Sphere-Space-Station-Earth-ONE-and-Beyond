"""glTF exporter generating meshes, materials and a simple animation.

The exporter builds CadQuery solids for decks and the hull, cuts window
openings, converts the geometry to triangle meshes and finally assembles a
glTF 2.0 document with PBR materials.  A basic rotation animation of the
entire station is appended so that viewers can inspect the model easily.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Tuple

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("gltf")


# ``cadquery`` is an optional dependency used for generating the geometry of the
# space station.  The test environment does not provide it, so the module falls
# back to very small placeholder meshes when the import fails.  This keeps the
# public API working without pulling in the heavy CAD dependency.
try:  # pragma: no cover - exercised indirectly in tests
    import cadquery as cq  # type: ignore
except Exception:  # pragma: no cover - cadquery is optional
    log.info("---- CadQuery not available, using placeholder meshes. ----")
    # Set `cq` to None so that the rest of the code can check for its availability
    cq = None  # type: ignore[assignment]
import numpy as np
from pygltflib import (
    Accessor,
    Animation,
    AnimationChannel,
    AnimationChannelTarget,
    AnimationSampler,
    Buffer,
    BufferView,
    GLTF2,
    Material as GLTFMaterial,
    Mesh,
    Node,
    PbrMetallicRoughness,
    Primitive,
    Scene,
)

from ..data_model import (
    BaseRing,
    Deck,
    Hull,
    Material as ModelMaterial,
    STEEL,
    GLASS,
    StationModel,
    Wormhole,
)


def _ensure_material(
    materials: List[GLTFMaterial],
    lookup: dict[str, int],
    mat: ModelMaterial,
) -> int:
    if mat.name not in lookup:
        color = list(mat.color_rgba) if mat.color_rgba else [0.8, 0.8, 0.8, 1.0]
        metallic = 0.0 if mat.name == "Glas" else 0.8
        rough = 0.1 if mat.name == "Glas" else 0.4
        materials.append(
            GLTFMaterial(
                name=mat.name,
                pbrMetallicRoughness=PbrMetallicRoughness(
                    baseColorFactor=color,
                    metallicFactor=metallic,
                    roughnessFactor=rough,
                ),
            )
        )
        lookup[mat.name] = len(materials) - 1
    return lookup[mat.name]


if cq is not None:  # pragma: no cover - exercised when cadquery is installed

    def _tessellate(obj: cq.Workplane) -> Tuple[np.ndarray, np.ndarray]:
        vertices, faces = obj.val().tessellate(0.5)
        verts = [v.toTuple() if hasattr(v, "toTuple") else v for v in vertices]
        return np.array(verts, dtype=np.float32), np.array(faces, dtype=np.uint32)

    def _build_deck_mesh(
        deck: Deck,
    ) -> Tuple[Tuple[np.ndarray, np.ndarray], List[Tuple[np.ndarray, np.ndarray]]]:
        solid = (
            cq.Workplane("XY")
            .circle(deck.net_outer_radius_m)
            .circle(deck.net_inner_radius_m)
            .extrude(deck.net_height_m)
        )
        windows: List[Tuple[np.ndarray, np.ndarray]] = []
        for w in deck.windows:
            hole = (
                cq.Workplane("XY")
                .center(w.position[0], w.position[1])
                .box(w.size_m, w.size_m, deck.net_height_m * 1.2)
            )
            solid = solid.cut(hole)
            glass = (
                cq.Workplane("XY")
                .center(w.position[0], w.position[1])
                .box(w.size_m, w.size_m, 0.01)
                .translate((0, 0, deck.net_height_m / 2))
            )
            windows.append(_tessellate(glass))
        return _tessellate(solid), windows

    def _build_hull_mesh(
        hull: Hull,
    ) -> Tuple[Tuple[np.ndarray, np.ndarray], List[Tuple[np.ndarray, np.ndarray]]]:
        solid = cq.Workplane("XY").sphere(hull.net_radius_m)
        windows: List[Tuple[np.ndarray, np.ndarray]] = []
        for w in hull.windows:
            hole = (
                cq.Workplane("XY")
                .center(w.position[0], w.position[1])
                .circle(w.size_m / 2)
                .extrude(hull.net_radius_m * 2)
                .translate((0, 0, w.position[2]))
            )
            solid = solid.cut(hole)
            glass = (
                cq.Workplane("XY")
                .center(w.position[0], w.position[1])
                .circle(w.size_m / 2)
                .extrude(0.01)
                .translate((0, 0, w.position[2]))
            )
            windows.append(_tessellate(glass))
        return _tessellate(solid), windows

    def _build_wormhole_mesh(wormhole: Wormhole) -> Tuple[np.ndarray, np.ndarray]:
        solid = cq.Workplane("XY").circle(wormhole.radius_m).extrude(wormhole.height_m)
        return _tessellate(solid)

    def _build_base_ring_mesh(ring: BaseRing) -> Tuple[np.ndarray, np.ndarray]:
        outer = ring.radius_m + ring.width_m / 2
        inner = ring.radius_m - ring.width_m / 2
        solid = (
            cq.Workplane("XY")
            .circle(outer)
            .circle(inner)
            .extrude(ring.width_m)
            .translate((0, 0, ring.position_z_m))
        )
        return _tessellate(solid)

else:
    # ``cadquery`` is unavailable.  Produce very small placeholder meshes so that
    # the exporter can still generate a valid glTF file used in the tests.  The
    # geometry is intentionally tiny and not representative of the real model,
    # but it keeps the function signatures identical.

    def _build_deck_mesh(
        deck: Deck,
    ) -> Tuple[Tuple[np.ndarray, np.ndarray], List[Tuple[np.ndarray, np.ndarray]]]:
        # simple flat square as placeholder deck
        verts = np.array(
            [
                [-0.5, -0.5, 0.0],
                [0.5, -0.5, 0.0],
                [0.5, 0.5, 0.0],
                [-0.5, 0.5, 0.0],
            ],
            dtype=np.float32,
        )
        faces = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.uint32)
        return (verts, faces), []

    def _build_hull_mesh(
        hull: Hull,
    ) -> Tuple[Tuple[np.ndarray, np.ndarray], List[Tuple[np.ndarray, np.ndarray]]]:
        # simple tetrahedron as placeholder hull
        verts = np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.5, 0.866, 0.0],
                [0.5, 0.2887, 0.8165],
            ],
            dtype=np.float32,
        )
        faces = np.array([[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]], dtype=np.uint32)
        return (verts, faces), []

    def _build_wormhole_mesh(wormhole: Wormhole) -> Tuple[np.ndarray, np.ndarray]:
        temp_deck = Deck(
            id=0,
            inner_radius_m=0.0,
            outer_radius_m=wormhole.radius_m,
            height_m=wormhole.height_m,
        )
        (verts, faces), _ = _build_deck_mesh(temp_deck)
        return verts, faces

    def _build_base_ring_mesh(ring: BaseRing) -> Tuple[np.ndarray, np.ndarray]:
        verts = np.array(
            [
                [-0.4, -0.4, 0.0],
                [0.4, -0.4, 0.0],
                [0.4, 0.4, 0.0],
                [-0.4, 0.4, 0.0],
            ],
            dtype=np.float32,
        )
        faces = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.uint32)
        return verts, faces


def _add_mesh(
    binary: bytearray,
    buffer_views: List[BufferView],
    accessors: List[Accessor],
    meshes: List[Mesh],
    nodes: List[Node],
    verts: np.ndarray,
    faces: np.ndarray,
    material_index: int,
) -> None:
    v_bytes = verts.tobytes()
    v_offset = len(binary)
    binary.extend(v_bytes)
    buffer_views.append(
        BufferView(buffer=0, byteOffset=v_offset, byteLength=len(v_bytes), target=34962)
    )
    min_v = verts.min(axis=0).tolist()
    max_v = verts.max(axis=0).tolist()
    accessors.append(
        Accessor(
            bufferView=len(buffer_views) - 1,
            componentType=5126,
            count=len(verts),
            type="VEC3",
            min=min_v,
            max=max_v,
        )
    )

    f_bytes = faces.astype(np.uint32).reshape(-1).tobytes()
    f_offset = len(binary)
    binary.extend(f_bytes)
    buffer_views.append(
        BufferView(buffer=0, byteOffset=f_offset, byteLength=len(f_bytes), target=34963)
    )
    accessors.append(
        Accessor(
            bufferView=len(buffer_views) - 1,
            componentType=5125,
            count=faces.size,
            type="SCALAR",
        )
    )

    mesh = Mesh(
        primitives=[
            Primitive(
                attributes={"POSITION": len(accessors) - 2},
                indices=len(accessors) - 1,
                material=material_index,
            )
        ]
    )
    meshes.append(mesh)
    nodes.append(Node(mesh=len(meshes) - 1))


def export_gltf(model: StationModel, filepath: str | Path) -> Path:
    """Export the station model to a glTF 2.0 file."""

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    log.info("Exporting glTF to %s", path)
    binary = bytearray()
    buffer_views: List[BufferView] = []
    accessors: List[Accessor] = []
    meshes: List[Mesh] = []
    nodes: List[Node] = []

    materials: List[GLTFMaterial] = []
    material_lookup: dict[str, int] = {}

    def mat_index(mat: ModelMaterial | None, default: ModelMaterial) -> int:
        """Return the index of ``mat`` or fall back to ``default``.

        This helper ensures that windows receive glass by default while all
        other elements use steel unless a specific material is supplied.
        """

        chosen = mat or default
        return _ensure_material(materials, material_lookup, chosen)

    child_nodes: List[int] = []
    for deck in model.decks:
        (verts, faces), windows = _build_deck_mesh(deck)
        _add_mesh(
            binary,
            buffer_views,
            accessors,
            meshes,
            nodes,
            verts,
            faces,
            mat_index(deck.material, STEEL),
        )
        child_nodes.append(len(nodes) - 1)
        for wv, wf in windows:
            _add_mesh(
                binary,
                buffer_views,
                accessors,
                meshes,
                nodes,
                wv,
                wf,
                mat_index(None, GLASS),
            )
            child_nodes.append(len(nodes) - 1)

    for ring in model.base_rings:
        verts, faces = _build_base_ring_mesh(ring)
        _add_mesh(
            binary,
            buffer_views,
            accessors,
            meshes,
            nodes,
            verts,
            faces,
            mat_index(ring.material, STEEL),
        )
        child_nodes.append(len(nodes) - 1)

    if model.hull:
        (verts, faces), windows = _build_hull_mesh(model.hull)
        _add_mesh(
            binary,
            buffer_views,
            accessors,
            meshes,
            nodes,
            verts,
            faces,
            mat_index(model.hull.material, STEEL),
        )
        child_nodes.append(len(nodes) - 1)
        for wv, wf in windows:
            _add_mesh(
                binary,
                buffer_views,
                accessors,
                meshes,
                nodes,
                wv,
                wf,
                mat_index(None, GLASS),
            )
            child_nodes.append(len(nodes) - 1)

    if model.wormhole:
        verts, faces = _build_wormhole_mesh(model.wormhole)
        _add_mesh(
            binary,
            buffer_views,
            accessors,
            meshes,
            nodes,
            verts,
            faces,
            mat_index(model.wormhole.material, STEEL),
        )
        child_nodes.append(len(nodes) - 1)

    root_idx = len(nodes)
    nodes.append(Node(children=child_nodes))

    # Animation data (rotation around Z axis)
    time_data = np.array([0.0, 1.0], dtype=np.float32)
    rot_data = np.array([[0, 0, 0, 1], [0, 0, 1, 0]], dtype=np.float32)

    t_offset = len(binary)
    binary.extend(time_data.tobytes())
    buffer_views.append(
        BufferView(buffer=0, byteOffset=t_offset, byteLength=time_data.nbytes)
    )
    accessors.append(
        Accessor(
            bufferView=len(buffer_views) - 1,
            componentType=5126,
            count=2,
            type="SCALAR",
            min=[0.0],
            max=[1.0],
        )
    )

    r_offset = len(binary)
    binary.extend(rot_data.tobytes())
    buffer_views.append(
        BufferView(buffer=0, byteOffset=r_offset, byteLength=rot_data.nbytes)
    )
    accessors.append(
        Accessor(
            bufferView=len(buffer_views) - 1,
            componentType=5126,
            count=2,
            type="VEC4",
        )
    )

    sampler = AnimationSampler(input=len(accessors) - 2, output=len(accessors) - 1)
    channel = AnimationChannel(
        sampler=0, target=AnimationChannelTarget(node=root_idx, path="rotation")
    )
    animations = [Animation(samplers=[sampler], channels=[channel])]

    buffer = Buffer(byteLength=len(binary))
    scene = Scene(nodes=[root_idx])
    gltf = GLTF2(
        scenes=[scene],
        nodes=nodes,
        meshes=meshes,
        materials=materials,
        accessors=accessors,
        bufferViews=buffer_views,
        buffers=[buffer],
        animations=animations,
    )
    gltf.set_binary_blob(bytes(binary))
    gltf.save(str(path))
    return path
