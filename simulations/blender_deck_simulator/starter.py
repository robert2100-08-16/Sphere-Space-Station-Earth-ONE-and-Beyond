import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

# Allow execution without installing the package by adding the repository root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from simulations.sphere_space_station_simulations import SphereDeckCalculator
from simulations.sphere_space_station_simulations.adapters.gltf_exporter import (
    export_gltf,
)
from simulations.sphere_space_station_simulations.adapters.step_exporter import (
    export_step,
)
from simulations.sphere_space_station_simulations.data_model import (
    Deck,
    Hull,
    StationModel,
)
from simulations.blender_deck_simulator.prepare_blender_scene import prepare_scene


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Launch Blender with the deck simulation script",
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
        "--background",
        action="store_true",
        help="Run Blender in background mode",
    )
    parser.add_argument(
        "--export-step",
        help="Write a STEP file with the station geometry",
    )
    parser.add_argument(
        "--export-gltf",
        help="Write a glTF file with the station geometry",
    )
    parser.add_argument("--export-json", help="Write the station data model as JSON")
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Additional arguments forwarded to Blender",
    )

    args = parser.parse_args()

    calculator = SphereDeckCalculator(
        "Deck Dimensions of a Sphere",
        sphere_diameter=127.0,
        hull_thickness=0.5,
        windows_per_deck_ratio=0.20,
        num_decks=16,
        deck_000_outer_radius=10.5,
        deck_height_brutto=3.5,
        deck_ceiling_thickness=0.5,
    )
    calculator.calculate_dynamics_of_a_sphere(angular_velocity=0.5)

    model = StationModel(
        decks=[
            Deck(
                id=int(row[SphereDeckCalculator.DECK_ID_LABEL].split("_")[1]),
                inner_radius_m=row[SphereDeckCalculator.INNER_RADIUS_LABEL],
                outer_radius_m=row[SphereDeckCalculator.OUTER_RADIUS_LABEL],
                height_m=row[SphereDeckCalculator.DECK_HEIGHT_LABEL],
            )
            for _, row in calculator.df_decks.iterrows()
        ],
        hull=Hull(radius_m=calculator.sphere_diameter / 2),
    )

    if args.export_step:
        export_step(model, Path(args.export_step))
    if args.export_gltf:
        export_gltf(model, Path(args.export_gltf))
    if args.export_json:
        with Path(args.export_json).open("w", encoding="utf-8") as fh:
            json.dump(asdict(model), fh, indent=2)

    script_dir = os.path.dirname(__file__)
    prepare_scene(os.path.join(script_dir, "station.glb"))

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
