"""adapter.py
A minimal Blender script that creates a simplified hull based on the
`deck_3d_construction_data.csv` file.

Run this script inside Blender or from the command line with
``blender --python adapter.py``.
"""

import csv
import os
import bpy


def load_outer_radius(csv_path: str) -> float:
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            raise ValueError("CSV contains no deck data")
        outer = float(rows[-1]["outer_radius_m"])
        return outer


def create_hull(radius: float) -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False)


def main() -> None:
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, "deck_3d_construction_data.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)
    radius = load_outer_radius(csv_path)
    create_hull(radius)


if __name__ == "__main__":
    main()
