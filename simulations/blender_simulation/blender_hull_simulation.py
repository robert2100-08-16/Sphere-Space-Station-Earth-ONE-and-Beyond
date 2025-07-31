"""blender_hull_simulation.py
---------------------------

Generate a simplified hull representation of the Sphere Station. The script can
optionally create windows and attach external aggregates such as radiators and
solar arrays. It is meant to be executed within Blender's Python environment.

Example command line usage:

```
blender --python blender_hull_simulation.py -- --windows --radiators --solar-arrays
```
"""

import argparse
import math
import bpy


def clear_scene() -> None:
    """Remove all objects from the current Blender scene."""

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def move_to_collection(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    """Link an object to a collection and unlink it from all others."""

    collection.objects.link(obj)
    for coll in list(obj.users_collection):
        if coll != collection:
            coll.objects.unlink(obj)


def create_hull(
    radius_m: float, thickness_m: float, name: str = "Hull"
) -> bpy.types.Object:
    """Create a spherical hull with the given radius and wall thickness."""

    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius_m, location=(0.0, 0.0, 0.0))
    outer = bpy.context.active_object
    outer.name = f"{name}_outer"

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius_m - thickness_m, location=(0.0, 0.0, 0.0)
    )
    inner = bpy.context.active_object
    inner.name = f"{name}_inner"

    boolean = outer.modifiers.new(name="Boolean", type="BOOLEAN")
    boolean.object = inner
    boolean.operation = "DIFFERENCE"
    bpy.context.view_layer.objects.active = outer
    bpy.ops.object.modifier_apply(modifier=boolean.name)

    inner.select_set(True)
    bpy.ops.object.delete()

    outer.name = name
    return outer


def create_window_ring(
    radius_m: float,
    num_windows: int,
    width_m: float,
    height_m: float,
    collection: bpy.types.Collection,
    name_prefix: str = "Window",
) -> None:
    """Create simple rectangular window placeholders around the hull."""

    if num_windows <= 0:
        return
    for i in range(num_windows):
        angle = math.radians(i * 360.0 / num_windows)
        x = radius_m * math.cos(angle)
        y = radius_m * math.sin(angle)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 0.0))
        win = bpy.context.active_object
        win.scale = (width_m / 2.0, width_m / 2.0, height_m / 2.0)
        win.rotation_euler[2] = angle
        win.name = f"{name_prefix}_{i:03d}"
        move_to_collection(win, collection)


def create_radiator(
    radius_m: float, length_m: float, width_m: float, angle_deg: float, name: str
) -> bpy.types.Object:
    """Create a simple radiator panel."""

    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(radius_m, 0.0, 0.0))
    panel = bpy.context.active_object
    panel.scale = (length_m / 2.0, width_m / 2.0, 1.0)
    panel.rotation_euler[2] = math.radians(angle_deg)
    panel.name = name
    return panel


def create_solar_array(
    radius_m: float, length_m: float, width_m: float, angle_deg: float, name: str
) -> bpy.types.Object:
    """Create a simple solar array panel."""

    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(radius_m, 0.0, 0.0))
    panel = bpy.context.active_object
    panel.scale = (length_m / 2.0, width_m / 2.0, 1.0)
    panel.rotation_euler[2] = math.radians(angle_deg)
    panel.name = name
    return panel


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualise the station hull")
    parser.add_argument("--windows", action="store_true", help="generate hull windows")
    parser.add_argument("--radiators", action="store_true", help="add radiator panels")
    parser.add_argument(
        "--solar-arrays",
        dest="solar_arrays",
        action="store_true",
        help="add solar array panels",
    )
    parser.add_argument(
        "--num-windows", type=int, default=8, help="number of windows to create"
    )
    parser.add_argument(
        "--radius", type=float, default=63.5, help="outer hull radius in metres"
    )
    parser.add_argument(
        "--thickness", type=float, default=1.0, help="hull wall thickness in metres"
    )
    args, _ = parser.parse_known_args()

    clear_scene()

    collection = bpy.data.collections.new("HullCollection")
    bpy.context.scene.collection.children.link(collection)

    hull = create_hull(args.radius, args.thickness)
    move_to_collection(hull, collection)

    if args.windows:
        create_window_ring(
            radius_m=args.radius - args.thickness / 2.0,
            num_windows=args.num_windows,
            width_m=1.0,
            height_m=3.0,
            collection=collection,
            name_prefix="Hull",
        )

    if args.radiators:
        rad1 = create_radiator(args.radius + 2.0, 10.0, 4.0, 0.0, "Radiator_1")
        rad2 = create_radiator(args.radius + 2.0, 10.0, 4.0, 180.0, "Radiator_2")
        move_to_collection(rad1, collection)
        move_to_collection(rad2, collection)

    if args.solar_arrays:
        sa1 = create_solar_array(args.radius + 3.0, 12.0, 5.0, 90.0, "SolarArray_1")
        sa2 = create_solar_array(args.radius + 3.0, 12.0, 5.0, -90.0, "SolarArray_2")
        move_to_collection(sa1, collection)
        move_to_collection(sa2, collection)


if __name__ == "__main__":
    main()
