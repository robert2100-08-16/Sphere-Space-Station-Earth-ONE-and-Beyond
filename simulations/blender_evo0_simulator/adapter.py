"""Blender adapter importing Evolution 00 GLB files as separate collections."""

from __future__ import annotations

import argparse
from pathlib import Path

try:  # pragma: no cover - Blender required
    import bpy  # type: ignore
except Exception:  # pragma: no cover - Blender not available
    bpy = None  # type: ignore[assignment]


def import_glb(path: Path) -> None:
    """Import a single GLB/GLTF file into Blender."""
    if bpy is None:  # pragma: no cover - Blender required
        raise ModuleNotFoundError("bpy module is required")
    bpy.ops.import_scene.gltf(filepath=str(path), import_scene_as_collection=True)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Import Evolution 00 GLB files")
    parser.add_argument(
        "paths",
        nargs="*",
        help="GLB files or directories containing them; defaults to results/evolutions/evolution-00",
    )
    args = parser.parse_args(argv)

    if bpy is None:  # pragma: no cover - Blender required
        raise ModuleNotFoundError("bpy module is required")

    to_import: list[Path] = []
    if args.paths:
        for p in args.paths:
            path = Path(p)
            if path.is_dir():
                to_import.extend(sorted(path.glob("*.glb")))
            else:
                to_import.append(path)
    else:
        default_dir = (
            Path(__file__).resolve().parent
            / ".."
            / "results"
            / "evolutions"
            / "evolution-00"
        )
        to_import.extend(sorted(default_dir.glob("*.glb")))

    for glb in to_import:
        import_glb(glb)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
