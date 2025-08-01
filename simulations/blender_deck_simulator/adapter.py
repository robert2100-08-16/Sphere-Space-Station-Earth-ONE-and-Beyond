"""
adapter.py
==========

This script generates a simplified 3D representation of the Sphere Station's deck
geometry using Blender's Python API.  It reads a comma‑separated file that
contains radial dimensions for each deck together with some additional
metadata (usage, material selection, etc.) and constructs hollow cylindrical
shells around a central ``wormhole``.  The resulting scene consists of
coaxial cylinders sharing the same centre rather than being stacked along the
Z‑axis.  The scene contains:

* A central ``wormhole`` cylinder that runs through the entire station.
* Deck shells modelled as the difference between two concentric cylinders.
* Top and bottom base rings sized relative to the wormhole radius.

The script is designed to be executed inside Blender.  Launch Blender, open
``Scripting`` workspace and run this script (or execute with
``blender --python adapter.py`` from the command line).  The
script assumes the unit system in Blender is set to metric and uses metres
throughout.

Dependencies
------------

The script uses only built‑in Blender modules.  If you wish to read the CSV
using pandas, install it and adjust the loader accordingly.  For the current
implementation we use Python's built‑in ``csv`` module to avoid external
dependencies.

Input CSV
---------

The CSV used by this script should contain, at minimum, the following columns:

* ``deck_id`` – unique name (e.g. ``Deck_001``)
* ``inner_radius_m`` – radial distance from the centre to the inner wall of the deck
* ``outer_radius_m`` – radial distance to the outer wall of the deck
* ``deck_height_m`` – overall vertical deck height (brutto)

Additional columns (usage, materials, etc.) are ignored by the script but
present in the example input for completeness.

Folder Structure
----------------

Place this file inside ``simulations/blender_deck_simulator`` together with
``deck_3d_construction_data.csv``.  The typical structure is:

```
simulations/
└── blender_deck_simulator/
    ├── adapter.py
    ├── deck_3d_construction_data.csv
    └── README.md
```

Usage
-----

In Blender's Python console or as a command line invocation:

.. code:: bash

   blender --python adapter.py

Alternatively, run this script from inside Blender's Scripting workspace.  A
collection named ``SphereDeckCollection`` will be created containing all
generated objects.  You can further refine the geometry, assign materials or
add modifiers within Blender.
"""

import csv
import os
import math
import bpy

from simulations.sphere_space_station_simulations.blender_helpers import (
    acceleration_to_color,
    clear_scene,
    move_to_collection,
    get_or_create_material,
    assign_material,
    create_window_strip,
    create_radiator,
    create_solar_array,
    create_smr,
    create_rotation_controller,
    add_light,
    create_ring_deck,
    create_wormhole,
    create_base_rings,
)




def load_deck_data(csv_path: str) -> list:
    """Load deck information from a CSV file.

    Returns a list of dictionaries with geometry and material information.
    """
    decks = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            deck_info = {
                "deck_id": row["deck_id"],
                "inner_radius_m": float(row["inner_radius_m"]),
                "outer_radius_m": float(row["outer_radius_m"]),
                "outer_radius_netto_m": float(row["outer_radius_netto_m"]),
                "deck_height_m": float(row["deck_height_m"]),
                "num_windows": int(row.get("num_windows", 0)),
                "window_thickness_cm": float(row.get("window_thickness_cm", 0)),
                "structure_material": row.get("structure_material", ""),
                "rotation_velocity_mps": float(row.get("rotation_velocity_mps", 0)),
                "centrifugal_acceleration_mps2": float(
                    row.get("centrifugal_acceleration_mps2", 0)
                ),
            }
            decks.append(deck_info)
    return decks


def main():
    # Determine the path to the CSV relative to this script
    script_dir = (
        os.path.dirname(bpy.data.filepath)
        if bpy.data.is_saved
        else os.path.dirname(__file__)
    )
    csv_path = os.path.join(script_dir, "deck_3d_construction_data.csv")

    # If the CSV does not exist, abort
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Load deck information
    decks = load_deck_data(csv_path)

    # Clean the scene
    clear_scene()

    # Create a new collection for organisation
    collection = bpy.data.collections.new("SphereDeckCollection")
    bpy.context.scene.collection.children.link(collection)

    # Determine the sphere's inner radius from the outermost deck.  Each deck
    # cylinder should end where it intersects the inner hull.  Compute the
    # appropriate height individually so that the cylinders do not extend
    # beyond the hull.
    sphere_radius = decks[-1]["outer_radius_m"]
    total_height_m = 2 * sphere_radius
    created_decks = []
    rotation_ctrl = create_rotation_controller()
    for deck in decks:
        calc_height_m = (
            2 * max(sphere_radius**2 - deck["outer_radius_m"] ** 2, 0.0) ** 0.5
        )
        obj = create_ring_deck(
            outer_radius_m=deck["outer_radius_m"],
            inner_radius_m=deck["inner_radius_m"],
            deck_height_m=calc_height_m,
            z_center_m=0.0,
            name=deck["deck_id"],
        )
        created_decks.append(obj)
        move_to_collection(obj, collection)
        obj.parent = rotation_ctrl

        # Assign structure material using colour mapped from acceleration
        color = acceleration_to_color(deck["centrifugal_acceleration_mps2"])
        assign_material(obj, deck["structure_material"], color)

        # Create windows up to Deck 012
        if int(deck["deck_id"].split()[1]) <= 12:
            create_window_strip(
                deck_radius_m=deck["outer_radius_netto_m"],
                window_thickness_cm=deck["window_thickness_cm"],
                deck_height_m=deck["deck_height_m"],
                num_windows=deck["num_windows"],
                angle_offset_deg=0.0,
                name_prefix=deck["deck_id"],
                collection=collection,
            )

    # Create wormhole cylinder through all decks
    wormhole_radius_m = (
        decks[0]["outer_radius_m"]
        - (decks[0]["outer_radius_m"] - decks[0]["inner_radius_m"]) * 0.5
    )
    wormhole = create_wormhole(wormhole_radius_m, total_height_m)
    move_to_collection(wormhole, collection)
    wormhole.parent = rotation_ctrl

    # Create base rings
    base_thickness_m = 2.0  # metres
    rings = create_base_rings(wormhole_radius_m, base_thickness_m, total_height_m)
    for ring in rings:
        move_to_collection(ring, collection)
        ring.parent = rotation_ctrl

    # Add simple energy and thermal systems
    rad1 = create_radiator(sphere_radius * 1.1, 10.0, 4.0, 0.0, "Radiator_1")
    rad2 = create_radiator(sphere_radius * 1.1, 10.0, 4.0, 180.0, "Radiator_2")
    move_to_collection(rad1, collection)
    move_to_collection(rad2, collection)
    rad1.parent = rotation_ctrl
    rad2.parent = rotation_ctrl

    solar1 = create_solar_array(sphere_radius * 1.2, 12.0, 5.0, 90.0, "SolarArray_1")
    solar2 = create_solar_array(sphere_radius * 1.2, 12.0, 5.0, -90.0, "SolarArray_2")
    move_to_collection(solar1, collection)
    move_to_collection(solar2, collection)
    solar1.parent = rotation_ctrl
    solar2.parent = rotation_ctrl

    smr = create_smr(height_m=4.0, radius_m=2.0)
    move_to_collection(smr, collection)
    smr.parent = rotation_ctrl

    # Lights for basic illumination
    add_light("TopLight", (0.0, 0.0, total_height_m / 2.0 + 2.0), 2000.0)
    add_light("BottomLight", (0.0, 0.0, -(total_height_m / 2.0 + 2.0)), 2000.0)

    # Animate rotation using outermost deck velocity
    outer_velocity = decks[-1]["rotation_velocity_mps"]
    period_seconds = (2 * math.pi * sphere_radius) / max(outer_velocity, 0.1)
    fps = bpy.context.scene.render.fps
    frame_end = int(period_seconds * fps)
    rotation_ctrl.rotation_euler[2] = 0.0
    rotation_ctrl.keyframe_insert(data_path="rotation_euler", frame=1)
    rotation_ctrl.rotation_euler[2] = 2 * math.pi
    rotation_ctrl.keyframe_insert(data_path="rotation_euler", frame=frame_end)


# Only execute when run inside Blender (not on import)
if __name__ == "__main__":
    main()
