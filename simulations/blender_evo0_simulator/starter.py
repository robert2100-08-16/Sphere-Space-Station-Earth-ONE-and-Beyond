import argparse
import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch Blender for Evolution 00")
    parser.add_argument(
        "--blender",
        default=os.getenv("BLENDER_PATH"),
        help="Path to the Blender executable (or set BLENDER_PATH)",
    )
    parser.add_argument(
        "--file",
        default=os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "results", 
            "evolutions",
            "evolution-00",
            "deck000_ev0.glb"
        ),
        help="GLB file to import",
    )
    parser.add_argument(
        "--background", 
        action="store_true", 
        help="Run Blender in background mode"
    )

    args = parser.parse_args()

    blender = args.blender
    if not blender:
        print("BLENDER_PATH not set and --blender not provided", file=sys.stderr)
        sys.exit(1)

    # Convert file path to forward slashes for Blender
    file_path = str(Path(args.file).resolve()).replace('\\', '/')

    # Prepare Python script based on file type
    script = "import bpy; bpy.ops.wm.read_factory_settings(); "
    if file_path.lower().endswith('.glb'):
        script += f"bpy.ops.import_scene.gltf(filepath='{file_path}', import_scene_as_collection=True); "
    else:
        script += f"bpy.ops.wm.open_mainfile(filepath='{file_path}'); "
    script += "bpy.ops.wm.save_mainfile(filepath='output2.blend');"

    # Command line arguments in correct order
    cmd = [
        blender,  # Blender executable
    ]
    if args.background:
        cmd.append("--background")
    cmd.extend([
        "--python-expr", script
    ])

    try:
        print(f"Running Blender with command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Blender command failed: {e}", file=sys.stderr)
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
