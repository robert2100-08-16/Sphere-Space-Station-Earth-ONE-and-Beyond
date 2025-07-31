import argparse
from typing import Any
from simulations.scripts.deck_calculations_script import SphereDeckCalculator


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


if __name__ == "__main__":
    main()
