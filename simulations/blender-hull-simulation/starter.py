import argparse
import csv
import json
import os
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

# Allow execution without installing the package by adding the repository root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from simulations.sphere_space_station_simulations.adapters.gltf_exporter import (
    export_gltf,
)
from simulations.sphere_space_station_simulations.adapters.step_exporter import (
    export_step,
)
from simulations.sphere_space_station_simulations.data_model import Deck, Hull, StationModel


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Launch Blender with the hull simulation script"
    )
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
        "--export-step", help="Write a STEP file with the station geometry"
    )
    parser.add_argument(
        "--export-gltf", help="Write a glTF file with the station geometry"
    )
    parser.add_argument(
        "--export-json", help="Write the station data model as JSON"
    )
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Additional arguments forwarded to Blender",
    )

    args = parser.parse_args()

    csv_path = os.path.join(os.path.dirname(__file__), "deck_3d_construction_data.csv")
    with open(csv_path, newline="") as fh:
        rows = list(csv.DictReader(fh))

    model = StationModel(
        decks=[
            Deck(
                id=int(row["deck_id"].split()[1]),
                inner_radius_m=float(row["inner_radius_m"]),
                outer_radius_m=float(row["outer_radius_m"]),
                height_m=float(row["deck_height_m"]),
            )
            for row in rows
        ],
        hull=Hull(radius_m=float(rows[-1]["outer_radius_m"])) if rows else None,
    )

    if args.export_step:
        export_step(model, Path(args.export_step))
    if args.export_gltf:
        export_gltf(model, Path(args.export_gltf))
    if args.export_json:
        with Path(args.export_json).open("w", encoding="utf-8") as fh:
            json.dump(asdict(model), fh, indent=2)

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
