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

* ``deck_id`` – unique name (e.g. ``Deck_001``)
* ``inner_radius_m`` – radial distance from the centre to the inner wall of the deck
* ``outer_radius_m`` – radial distance to the outer wall of the deck
* ``deck_height_m`` – overall vertical deck height (brutto)

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
import math
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


def get_or_create_material(
    name: str, color: tuple[float, float, float, float]
) -> bpy.types.Material:
    """Return existing material or create a new one with the given RGBA color."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs[0].default_value = color
    return mat


def assign_material(
    obj: bpy.types.Object,
    material_name: str,
    color: tuple[float, float, float, float],
) -> None:
    """Assign material to the given object."""
    mat = get_or_create_material(material_name, color)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def create_window_strip(
    deck_radius_m: float,
    window_thickness_cm: float,
    deck_height_m: float,
    num_windows: int,
    angle_offset_deg: float,
    name_prefix: str,
    collection: bpy.types.Collection,
) -> None:
    """Create rectangular window openings along the deck wall."""
    if num_windows <= 0:
        return
    width_m = window_thickness_cm / 100.0
    height_m = deck_height_m * 0.5
    for i in range(num_windows):
        angle = math.radians(angle_offset_deg + i * 360.0 / num_windows)
        x = deck_radius_m * math.cos(angle)
        y = deck_radius_m * math.sin(angle)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 0.0))
        win = bpy.context.active_object
        win.scale = (width_m / 2.0, width_m / 2.0, height_m / 2.0)
        win.rotation_euler[2] = angle
        win.name = f"{name_prefix}_window_{i:03d}"
        move_to_collection(win, collection)


def create_radiator(
    radius_m: float,
    length_m: float,
    width_m: float,
    angle_deg: float,
    name: str,
) -> bpy.types.Object:
    """Create a simple radiator panel."""
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(radius_m, 0.0, 0.0))
    panel = bpy.context.active_object
    panel.scale = (length_m / 2.0, width_m / 2.0, 1.0)
    panel.rotation_euler[2] = math.radians(angle_deg)
    panel.name = name
    return panel


def create_solar_array(
    radius_m: float,
    length_m: float,
    width_m: float,
    angle_deg: float,
    name: str,
) -> bpy.types.Object:
    """Create a simple solar array panel."""
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(radius_m, 0.0, 0.0))
    panel = bpy.context.active_object
    panel.scale = (length_m / 2.0, width_m / 2.0, 1.0)
    panel.rotation_euler[2] = math.radians(angle_deg)
    panel.name = name
    return panel


def create_smr(height_m: float, radius_m: float) -> bpy.types.Object:
    """Create a simplified small modular reactor cylinder."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius_m, depth=height_m, location=(0.0, 0.0, -height_m / 2.0)
    )
    smr = bpy.context.active_object
    smr.name = "SMR"
    return smr


def create_rotation_controller() -> bpy.types.Object:
    """Create an empty object that controls station rotation."""
    bpy.ops.object.empty_add(type="PLAIN_AXES")
    ctrl = bpy.context.active_object
    ctrl.name = "RotationController"
    return ctrl


def add_light(
    name: str, location: tuple[float, float, float], energy: float = 1000.0
) -> bpy.types.Object:
    """Add a point light to the scene."""
    bpy.ops.object.light_add(type="POINT", location=location)
    light = bpy.context.active_object
    light.data.energy = energy
    light.name = name
    return light


def create_ring_deck(
    outer_radius_m: float,
    inner_radius_m: float,
    deck_height_m: float,
    z_center_m: float,
    name: str,
) -> bpy.types.Object:
    """Construct a hollow cylindrical shell using boolean difference.

    Args:
        outer_radius_m: Radius of the outer cylinder in metres.
        inner_radius_m: Radius of the inner cylinder to subtract.
        deck_height_m: Height of the deck (cylinder depth) in metres.
        z_center_m: Z‑axis position of the deck's centre in metres.
        name: Name assigned to the resulting mesh object.

    Returns:
        The resulting Blender object representing the deck shell.
    """
    # Create outer cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        radius=outer_radius_m,
        depth=deck_height_m,
        location=(0.0, 0.0, z_center_m),
    )
    outer = bpy.context.active_object
    outer.name = f"{name}_outer"

    # Create slightly taller inner cylinder for boolean subtraction
    # Extra height ensures the boolean operation fully cuts through
    bpy.ops.mesh.primitive_cylinder_add(
        radius=inner_radius_m,
        depth=deck_height_m + 0.05,
        location=(0.0, 0.0, z_center_m),
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


def create_wormhole(radius_m: float, total_height_m: float) -> bpy.types.Object:
    """Create the central wormhole cylinder running through all decks.

    The cylinder is centred at the origin so that all surrounding decks share
    the same vertical extent.
    """
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius_m, depth=total_height_m, location=(0.0, 0.0, 0.0)
    )
    wormhole = bpy.context.active_object
    wormhole.name = "Wormhole"
    return wormhole


def create_base_rings(
    wormhole_radius_m: float, base_thickness_m: float, total_height_m: float
) -> list:
    """Create upper and lower base rings at the ends of the wormhole.

    Args:
        wormhole_radius_m: Radius of the wormhole.
        base_thickness_m: Thickness of each base ring in metres.
        total_height_m: Total height of the station (inner diameter).

    Returns:
        List of ring objects created (top and bottom).
    """
    base_radius = wormhole_radius_m * 1.2
    rings = []
    half = total_height_m / 2.0
    for i, z_pos in enumerate(
        [half + base_thickness_m / 2.0, -(half + base_thickness_m / 2.0)]
    ):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=base_radius,
            depth=base_thickness_m,
            location=(0.0, 0.0, z_pos),
        )
        ring = bpy.context.active_object
        ring.name = f"BaseRing_{'Top' if i == 0 else 'Bottom'}"
        rings.append(ring)
    return rings


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

        # Assign structure material
        color = (0.2, 0.2, 0.2, 1.0)
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
