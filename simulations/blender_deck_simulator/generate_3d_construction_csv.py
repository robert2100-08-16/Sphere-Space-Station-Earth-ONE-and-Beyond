from pathlib import Path

from simulations.sphere_space_station_simulations.data_preparation import (
    generate_deck_construction_csv,
)

INPUT_CSV = Path(__file__).resolve().parents[1] / "results" / "deck_dimensions.csv"
OUTPUT_CSV = Path(__file__).resolve().parent / "deck_3d_construction_data.csv"


def main() -> None:
    path = generate_deck_construction_csv(INPUT_CSV, OUTPUT_CSV)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
