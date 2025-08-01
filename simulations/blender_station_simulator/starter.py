import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from simulations.sphere_space_station_simulations.simulation import main as station_main


def main() -> None:
    """Entry point delegating to :mod:`station_simulation`."""
    station_main(sys.argv[1:])


if __name__ == "__main__":
    main()
