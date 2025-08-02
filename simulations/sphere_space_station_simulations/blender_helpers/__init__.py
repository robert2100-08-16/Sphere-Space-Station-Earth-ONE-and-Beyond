"""Reusable Blender helper functions."""

from __future__ import annotations

import bpy
import math


def acceleration_to_color(acceleration: float) -> tuple[float, float, float, float]:
    """Return an RGBA color based on centrifugal acceleration."""
    ratio = max(acceleration / 9.81, 0.0)
    if ratio < 0.5:
        t = ratio / 0.5
        r, g, b = 1.0, 1.0, 1.0 - t
    elif ratio < 1.0:
        t = (ratio - 0.5) / 0.5
        r, g, b = 1.0 - t, 1.0, 0.0
    else:
        t = min((ratio - 1.0) / 1.0, 1.0)
        r, g, b = t, 1.0 - t, 0.0
    return (r, g, b, 1.0)


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
    obj: bpy.types.Object, material_name: str, color: tuple[float, float, float, float]
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
    """Construct a hollow cylindrical shell using boolean difference."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=outer_radius_m, depth=deck_height_m, location=(0.0, 0.0, z_center_m)
    )
    outer = bpy.context.active_object
    outer.name = f"{name}_outer"
    bpy.ops.mesh.primitive_cylinder_add(
        radius=inner_radius_m,
        depth=deck_height_m + 0.05,
        location=(0.0, 0.0, z_center_m),
    )
    inner = bpy.context.active_object
    inner.name = f"{name}_inner"
    boolean_mod = outer.modifiers.new(name="Boolean", type="BOOLEAN")
    boolean_mod.object = inner
    boolean_mod.operation = "DIFFERENCE"
    bpy.context.view_layer.objects.active = outer
    bpy.ops.object.modifier_apply(modifier=boolean_mod.name)
    bpy.data.objects.remove(inner, do_unlink=True)
    outer.name = name
    return outer


def create_wormhole(radius_m: float, total_height_m: float) -> bpy.types.Object:
    """Create the central wormhole cylinder running through all decks."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius_m, depth=total_height_m, location=(0.0, 0.0, 0.0)
    )
    wormhole = bpy.context.active_object
    wormhole.name = "Wormhole"
    return wormhole


def create_base_rings(
    wormhole_radius_m: float, base_thickness_m: float, total_height_m: float
) -> list:
    """Create upper and lower base rings at the ends of the wormhole."""
    base_radius = wormhole_radius_m * 1.2
    rings = []
    half = total_height_m / 2.0
    for i, z_pos in enumerate(
        [half + base_thickness_m / 2.0, -(half + base_thickness_m / 2.0)]
    ):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=base_radius, depth=base_thickness_m, location=(0.0, 0.0, z_pos)
        )
        ring = bpy.context.active_object
        ring.name = f"BaseRing_{'Top' if i == 0 else 'Bottom'}"
        rings.append(ring)
    return rings
