"""Utilities for preparing simulation data."""

from __future__ import annotations

import csv
import math
from pathlib import Path

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


def generate_deck_construction_csv(
    input_csv: str | Path, output_csv: str | Path
) -> Path:
    """Generate a CSV with additional deck metadata for Blender.

    Parameters
    ----------
    input_csv:
        Path to ``deck_dimensions.csv`` produced by the calculator.
    output_csv:
        Target path for ``deck_3d_construction_data.csv``.

    Returns
    -------
    Path
        The path of the written CSV file.
    """
    input_csv = Path(input_csv)
    output_csv = Path(output_csv)

    with open(input_csv, encoding="ISO-8859-1", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # drop descriptive header line
        header = next(reader)
        if header and header[0] == "":
            header = header[1:]
        rows = []
        for row in reader:
            if not row:
                continue
            if row[0] == "" or row[0].isdigit():
                row = row[1:]
            if not row or not row[0]:
                continue
            rows.append(dict(zip(header, row)))

    processed = []
    for i, row in enumerate(rows):
        if "inner_radius_m" not in row:
            continue
        inner = float(row["inner_radius_m"])
        outer = float(row["outer_radius_m"])
        outer_net = float(row["outer_radius_netto_m"])
        deck_inner_height = float(row["deck_inner_height_m"])
        rotation_velocity = float(row.get("rotation_velocity_mps", 0.0))
        accel = float(row.get("centrifugal_acceleration_mps2", 0.0))
        processed.append(
            {
                "deck_id": row["deck_id"],
                "deck_usage": USAGE_MAP.get(i, ""),
                "inner_radius_m": inner,
                "outer_radius_m": outer,
                "outer_radius_netto_m": outer_net,
                "deck_height_m": outer - inner,
                "deck_inner_height_m": deck_inner_height,
                "num_windows": math.floor(outer_net / 1.6),
                "window_material": WINDOW_MATERIAL,
                "window_thickness_cm": WINDOW_THICKNESS_CM,
                "structure_material": STRUCTURE_MATERIAL,
                "rotation_velocity_mps": rotation_velocity,
                "centrifugal_acceleration_mps2": accel,
            }
        )

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

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in processed:
            writer.writerow(row)
    return output_csv
