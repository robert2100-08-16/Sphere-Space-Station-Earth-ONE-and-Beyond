"""Blender adapter loading a glTF hull model.

The previous prototype read ``deck_3d_construction_data.csv`` and created a
primitive sphere based on the outer deck radius.  This version assumes that the
geometry has already been exported to a glTF file by ``gltf_exporter.py`` and
imports it directly using Blender's Python API.  After import a simple material
is assigned to all mesh objects so the model is immediately visible.

Run this script inside Blender or from the command line with
``blender --python adapter.py``.
"""

from __future__ import annotations

import argparse
import os
import sys

try:  # pragma: no cover - handled in tests
    import bpy  # type: ignore
except Exception:  # pragma: no cover - Blender not available
    bpy = None  # type: ignore[assignment]
try:
    from .prepare_blender_scene import prepare_scene
except ImportError:  # pragma: no cover - direct script execution
    script_path = os.path.dirname(__file__)
    sys.path.append(script_path)
    sys.path.append(os.path.abspath(os.path.join(script_path, "..", "..")))
    from prepare_blender_scene import prepare_scene


def import_gltf(filepath: str) -> None:
    """Import a glTF file using Blender's glTF importer."""

    if bpy is None:  # pragma: no cover - Blender required
        raise ModuleNotFoundError("bpy module is required")
    bpy.ops.import_scene.gltf(filepath=filepath)


def assign_basic_material(material_name: str = "HullMaterial") -> None:
    """Assign a simple material to all mesh objects.

    The material is created if it does not yet exist.
    """

    if bpy is None:  # pragma: no cover - Blender required
        raise ModuleNotFoundError("bpy module is required")

    mat = bpy.data.materials.get(material_name)
    if mat is None:
        mat = bpy.data.materials.new(name=material_name)
        mat.diffuse_color = (0.8, 0.8, 0.8, 1.0)

    for obj in bpy.data.objects:
        if obj.type == "MESH":
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--prepare", action="store_true", help="Generate scene and exit"
    )
    args, _ = parser.parse_known_args(argv)

    script_dir = os.path.dirname(__file__)
    gltf_path = os.path.join(script_dir, "station.glb")

    if args.prepare or not os.path.exists(gltf_path):
        prepare_scene(gltf_path)
        if args.prepare:
            return

    if not os.path.exists(gltf_path):
        raise FileNotFoundError(gltf_path)

    if bpy is None:  # pragma: no cover - Blender required
        raise ModuleNotFoundError("bpy module is required")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    import_gltf(gltf_path)
    assign_basic_material()


if __name__ == "__main__":
    main()
