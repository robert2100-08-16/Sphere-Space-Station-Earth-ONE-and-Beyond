import argparse
from pathlib import Path
from typing import Any

from simulations.sphere_space_station_simulations import SphereDeckCalculator
from simulations.sphere_space_station_simulations.adapters.gltf_exporter import (
    export_gltf,
)
from simulations.sphere_space_station_simulations.adapters.json_exporter import (
    export_json,
)
from simulations.sphere_space_station_simulations.adapters.step_exporter import (
    export_step,
)
from simulations.sphere_space_station_simulations.data_model import (
    Deck,
    Hull,
    StationModel,
)


class StationSimulation:
    """High level simulation integrating deck and hull models."""

    def __init__(
        self,
        enable_docking: bool = True,
        enable_mission_control: bool = True,
        enable_life_support: bool = True,
        enable_emergency_drills: bool = True,
    ) -> None:
        self.enable_docking = enable_docking
        self.enable_mission_control = enable_mission_control
        self.enable_life_support = enable_life_support
        self.enable_emergency_drills = enable_emergency_drills

        # Load deck and hull models using the existing calculator
        self.calculator = SphereDeckCalculator(
            "Deck Dimensions of a Sphere",
            sphere_diameter=127.0,
            hull_thickness=0.5,
            windows_per_deck_ratio=0.20,
            num_decks=16,
            deck_000_outer_radius=10.5,
            deck_height_brutto=3.5,
            deck_ceiling_thickness=0.5,
        )
        # Trigger calculation so geometry is available
        self.calculator.calculate_dynamics_of_a_sphere(angular_velocity=0.5)
        self.decks = self.calculator.df_decks
        self.hull = self.calculator.hull_geometry

    def simulate_docking(self) -> None:
        print("[Docking] Simulating spacecraft docking operations...")

    def run_mission_control(self) -> None:
        print("[Mission] Executing mission control scenario...")

    def run_life_support(self) -> None:
        print("[Life Support] Running life-support simulation...")

    def run_emergency_drills(self) -> None:
        print("[Emergency] Performing emergency drill sequence...")

    def run(self) -> None:
        if self.enable_docking:
            self.simulate_docking()
        if self.enable_mission_control:
            self.run_mission_control()
        if self.enable_life_support:
            self.run_life_support()
        if self.enable_emergency_drills:
            self.run_emergency_drills()

    def to_station_model(self) -> StationModel:
        return StationModel(
            decks=[
                Deck(
                    id=int(row[SphereDeckCalculator.DECK_ID_LABEL].split("_")[1]),
                    inner_radius_m=row[SphereDeckCalculator.INNER_RADIUS_LABEL],
                    outer_radius_m=row[SphereDeckCalculator.OUTER_RADIUS_LABEL],
                    height_m=row[SphereDeckCalculator.DECK_HEIGHT_LABEL],
                )
                for _, row in self.decks.iterrows()
            ],
            hull=Hull(radius_m=self.calculator.sphere_diameter / 2),
        )


def parse_args(args: Any | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sphere Station Simulation")
    parser.add_argument(
        "--no-docking",
        action="store_false",
        dest="docking",
        help="Disable spacecraft docking simulation",
    )
    parser.add_argument(
        "--no-mission-control",
        action="store_false",
        dest="mission_control",
        help="Disable mission control scenarios",
    )
    parser.add_argument(
        "--no-life-support",
        action="store_false",
        dest="life_support",
        help="Disable life-support simulation",
    )
    parser.add_argument(
        "--no-emergency",
        action="store_false",
        dest="emergency_drills",
        help="Disable emergency drills",
    )
    parser.add_argument(
        "--export-step", help="Write a STEP file with the station geometry"
    )
    parser.add_argument(
        "--export-gltf", help="Write a glTF file with the station geometry"
    )
    parser.add_argument("--export-json", help="Write the station data model as JSON")
    return parser.parse_args(args)


def main(args: Any | None = None) -> None:
    cli_args = parse_args(args)
    sim = StationSimulation(
        enable_docking=cli_args.docking,
        enable_mission_control=cli_args.mission_control,
        enable_life_support=cli_args.life_support,
        enable_emergency_drills=cli_args.emergency_drills,
    )
    sim.run()

    model = sim.to_station_model()
    if cli_args.export_step:
        export_step(model, Path(cli_args.export_step))
    if cli_args.export_gltf:
        export_gltf(model, Path(cli_args.export_gltf))
    if cli_args.export_json:
        export_json(model, Path(cli_args.export_json))


if __name__ == "__main__":
    main()
