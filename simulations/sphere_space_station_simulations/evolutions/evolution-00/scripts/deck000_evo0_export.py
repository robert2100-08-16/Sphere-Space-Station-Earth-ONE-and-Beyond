"""
Convenience runner to export EV0 artifacts without touching package internals.
"""

from pathlib import Path
from simulations.sphere_space_station_simulations.evolutions.evo0_deck000 import (
    build_and_export_ev0,
)


def main() -> None:
    out = build_and_export_ev0(Path("simulations/results/deck000_ev0"))
    for k, v in out.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
