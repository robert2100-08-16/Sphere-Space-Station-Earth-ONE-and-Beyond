import math
from pathlib import Path
import pandas as pd


INPUT_CSV = Path(__file__).resolve().parents[1] / "results" / "deck_dimensions.csv"
OUTPUT_CSV = Path(__file__).resolve().parent / "deck_3d_construction_data.csv"


USAGE_MAP = {
    0: "Docking & Command Center",
    1: "Residential/Operational",
    2: "Residential/Operational",
    3: "Residential/Operational",
    4: "Residential/Operational",
    5: "Residential/Operational",
    6: "Residential/Operational",
    7: "Residential/Operational",
    8: "Industrial/Recreational",
    9: "Industrial/Recreational",
    10: "Industrial/Recreational",
    11: "Industrial/Recreational",
    12: "Industrial/Recreational",
    13: "Storage/Propulsion",
    14: "Storage/Propulsion",
    15: "Storage/Propulsion",
}

WINDOW_MATERIAL = "ALON + Fused Silica + Polycarbonate + Borosilicate"
STRUCTURE_MATERIAL = "Silicon Carbide Composite + Silicon Elastomer"
WINDOW_THICKNESS_CM = 20


def main() -> None:
    df = pd.read_csv(INPUT_CSV, skiprows=1, encoding="ISO-8859-1")
    if df.columns[0].startswith("Unnamed"):
        df = df.drop(df.columns[0], axis=1)

    df = df[df["deck_id"].notna()].reset_index(drop=True)  # drop footer rows

    df["deck_usage"] = [USAGE_MAP.get(i, "") for i in range(len(df))]
    df["deck_height_m"] = df["outer_radius_m"] - df["inner_radius_m"]
    df["num_windows"] = [math.floor(r / 1.6) for r in df["outer_radius_netto_m"]]
    df["window_material"] = WINDOW_MATERIAL
    df["window_thickness_cm"] = WINDOW_THICKNESS_CM
    df["structure_material"] = STRUCTURE_MATERIAL

    cols = [
        "deck_id",
        "deck_usage",
        "inner_radius_m",
        "outer_radius_m",
        "outer_radius_netto_m",
        "deck_height_m",
        "deck_inner_height_m",
        "num_windows",
        "window_material",
        "window_thickness_cm",
        "structure_material",
        "rotation_velocity_mps",
        "centrifugal_acceleration_mps2",
    ]

    df[cols].to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
