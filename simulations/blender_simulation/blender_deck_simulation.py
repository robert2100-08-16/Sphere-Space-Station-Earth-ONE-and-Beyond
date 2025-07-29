"""
blender_deck_simulation.py
==========================

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
``blender --python blender_deck_simulation.py`` from the command line).  The
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

* ``Deck`` – unique name (e.g. ``Deck 001``)
* ``Inner Radius (m)`` – radial distance from the centre to the inner wall of the deck
* ``Outer Radius (m)`` – radial distance to the outer wall of the deck
* ``Deck Height (m)`` – overall vertical deck height (brutto)

Additional columns (usage, materials, etc.) are ignored by the script but
present in the example input for completeness.

Folder Structure
----------------

Place this file inside ``simulations/blender_simulation`` together with
``deck_3d_construction_data.csv``.  The typical structure is:

```
simulations/
└── blender_simulation/
    ├── blender_deck_simulation.py
    ├── deck_3d_construction_data.csv
    └── README.md
```

Usage
-----

In Blender's Python console or as a command line invocation:

.. code:: bash

   blender --python blender_deck_simulation.py

Alternatively, run this script from inside Blender's Scripting workspace.  A
collection named ``SphereDeckCollection`` will be created containing all
generated objects.  You can further refine the geometry, assign materials or
add modifiers within Blender.
"""

import csv
import os
import bpy


def clear_scene():
    """Remove all objects from the current Blender scene."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def move_to_collection(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    """Link an object to a collection and unlink it from all others."""
    collection.objects.link(obj)
    for coll in list(obj.users_collection):
        if coll != collection:
            coll.objects.unlink(obj)


def create_ring_deck(
    outer_radius: float, inner_radius: float, height: float, z_center: float, name: str
) -> bpy.types.Object:
    """Construct a hollow cylindrical shell using boolean difference.

    Args:
        outer_radius: Radius of the outer cylinder in metres.
        inner_radius: Radius of the inner cylinder to subtract.
        height: Height of the deck (cylinder depth) in metres.
        z_center: Z‑axis position of the deck's centre in metres.
        name: Name assigned to the resulting mesh object.

    Returns:
        The resulting Blender object representing the deck shell.
    """
    # Create outer cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        radius=outer_radius, depth=height, location=(0.0, 0.0, z_center)
    )
    outer = bpy.context.active_object
    outer.name = f"{name}_outer"

    # Create slightly taller inner cylinder for boolean subtraction
    # Extra height ensures the boolean operation fully cuts through
    bpy.ops.mesh.primitive_cylinder_add(
        radius=inner_radius, depth=height + 0.05, location=(0.0, 0.0, z_center)
    )
    inner = bpy.context.active_object
    inner.name = f"{name}_inner"

    # Add boolean modifier to outer cylinder
    boolean_mod = outer.modifiers.new(name="Boolean", type="BOOLEAN")
    boolean_mod.object = inner
    boolean_mod.operation = "DIFFERENCE"

    # Apply modifier
    bpy.context.view_layer.objects.active = outer
    bpy.ops.object.modifier_apply(modifier=boolean_mod.name)

    # Delete inner cylinder object
    inner.select_set(True)
    bpy.ops.object.delete()

    # Rename final object
    outer.name = name
    return outer


def create_wormhole(radius: float, total_height: float) -> bpy.types.Object:
    """Create the central wormhole cylinder running through all decks.

    The cylinder is centred at the origin so that all surrounding decks share
    the same vertical extent.
    """
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=total_height, location=(0.0, 0.0, 0.0)
    )
    wormhole = bpy.context.active_object
    wormhole.name = "Wormhole"
    return wormhole


def create_base_rings(
    wormhole_radius: float, base_thickness: float, total_height: float
) -> list:
    """Create upper and lower base rings at the ends of the wormhole.

    Args:
        wormhole_radius: Radius of the wormhole.
        base_thickness: Thickness of each base ring in metres.
        total_height: Total height of the station (inner diameter).

    Returns:
        List of ring objects created (top and bottom).
    """
    base_radius = wormhole_radius * 1.2
    rings = []
    half = total_height / 2.0
    for i, z_pos in enumerate(
        [half + base_thickness / 2.0, -(half + base_thickness / 2.0)]
    ):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=base_radius, depth=base_thickness, location=(0.0, 0.0, z_pos)
        )
        ring = bpy.context.active_object
        ring.name = f"BaseRing_{'Top' if i == 0 else 'Bottom'}"
        rings.append(ring)
    return rings


def load_deck_data(csv_path: str) -> list:
    """Load deck information from a CSV file.

    Returns a list of dictionaries with keys: deck_name, inner_radius,
    outer_radius, deck_height.
    """
    decks = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            deck_info = {
                "deck_name": row["Deck"],
                "inner_radius": float(row["Inner Radius (m)"]),
                "outer_radius": float(row["Outer Radius (m)"]),
                "height": float(row["Deck Height (m)"]),
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
    sphere_radius = decks[-1]["outer_radius"]
    total_height = 2 * sphere_radius
    created_decks = []
    for deck in decks:
        deck_height = 2 * max(sphere_radius**2 - deck["outer_radius"]**2, 0.0) ** 0.5
        obj = create_ring_deck(
            outer_radius=deck["outer_radius"],
            inner_radius=deck["inner_radius"],
            height=deck_height,
            z_center=0.0,
            name=deck["deck_name"],
        )
        created_decks.append(obj)
        move_to_collection(obj, collection)

    # Create wormhole cylinder through all decks
    wormhole_radius = (
        decks[0]["outer_radius"]
        - (decks[0]["outer_radius"] - decks[0]["inner_radius"]) * 0.5
    )
    wormhole = create_wormhole(wormhole_radius, total_height)
    move_to_collection(wormhole, collection)

    # Create base rings
    base_thickness = 2.0  # metres
    rings = create_base_rings(wormhole_radius, base_thickness, total_height)
    for ring in rings:
        move_to_collection(ring, collection)


# Only execute when run inside Blender (not on import)
if __name__ == "__main__":
    main()
