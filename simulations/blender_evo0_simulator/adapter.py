"""Blender adapter importing Evolution 00 GLB files as separate collections."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:  # pragma: no cover - Blender required
    import bpy  # type: ignore
except Exception:  # pragma: no cover - Blender not available
    bpy = None  # type: ignore[assignment]


def import_glb(path: Path) -> None:
    """Import a single GLB/GLTF file into Blender."""
    if bpy is None:  # pragma: no cover - Blender required
        raise ModuleNotFoundError("bpy module is required")
    
    try:
        print(f"Importing {path}...")
        bpy.ops.import_scene.gltf(filepath=str(path), import_scene_as_collection=True)
        print(f"Successfully imported {path}")
    except Exception as e:
        print(f"Error importing {path}: {e}", file=sys.stderr)
        raise


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
            path = Path(p).resolve()
            if path.is_dir():
                glb_files = list(sorted(path.glob("*.glb")))
                if not glb_files:
                    print(f"No .glb files found in directory: {path}", file=sys.stderr)
                to_import.extend(glb_files)
            else:
                if not path.exists():
                    print(f"File not found: {path}", file=sys.stderr)
                    continue
                if path.suffix.lower() != '.glb':
                    print(f"Warning: {path} is not a .glb file", file=sys.stderr)
                to_import.append(path)
    else:
        # Try multiple possible locations for GLB files
        possible_dirs = [
            # Relative to adapter.py
            Path(__file__).resolve().parent / ".." / "results" / "evolutions" / "evolution-00",
            # Relative to workspace root
            Path(__file__).resolve().parent / ".." / ".." / "results" / "evolutions" / "evolution-00",
            # Direct path
            Path("simulations/results/evolutions/evolution-00"),
        ]

        for dir in possible_dirs:
            if dir.exists():
                glb_files = list(sorted(dir.glob("*.glb")))
                if glb_files:
                    print(f"Found GLB files in {dir}")
                    to_import.extend(glb_files)
                    break
        
        if not to_import:
            print("No .glb files found in default locations:", file=sys.stderr)
            for dir in possible_dirs:
                print(f"  - {dir}", file=sys.stderr)
            sys.exit(1)

    if not to_import:
        print("No valid .glb files found to import", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(to_import)} GLB file(s) to import:")
    for glb in to_import:
        print(f"  - {glb}")
        import_glb(glb)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
