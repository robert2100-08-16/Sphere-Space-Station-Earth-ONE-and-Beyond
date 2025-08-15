import argparse
import os
import subprocess
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch Blender for Evolution 00")
    parser.add_argument(
        "--blender",
        default=os.getenv("BLENDER_PATH"),
        help="Path to the Blender executable (or set BLENDER_PATH)",
    )
    parser.add_argument(
        "--script",
        default=os.path.join(os.path.dirname(__file__), "adapter.py"),
        help="Blender Python file to execute",
    )
    parser.add_argument(
        "--background", action="store_true", help="Run Blender in background mode"
    )
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Additional arguments forwarded to Blender and the adapter",
    )

    args = parser.parse_args()

    blender = args.blender
    if not blender:
        print("BLENDER_PATH not set and --blender not provided", file=sys.stderr)
        sys.exit(1)

    cmd = [blender]
    if args.background:
        cmd.append("--background")
    cmd += ["--python", args.script]
    if args.extra:
        cmd += args.extra

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
