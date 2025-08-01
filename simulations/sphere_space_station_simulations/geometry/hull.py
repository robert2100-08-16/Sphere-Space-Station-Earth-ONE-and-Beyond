import numpy as np
import pandas as pd
from typing import Tuple


def calculate_hull_geometry(
    inner_sphere_diameter: float,
    df_decks: pd.DataFrame,
    outer_radius_netto_label: str = "outer_radius_netto_m",
    length_outer_radius_netto_label: str = "length_outer_radius_netto_m",
    num_points: int = 100,
) -> Tuple[np.ndarray, ...]:
    """Return coordinates for hull, central wormhole and base rings."""
    sphere_radius = inner_sphere_diameter / 2
    theta = np.linspace(0, 2 * np.pi, num_points)
    phi = np.linspace(0, np.pi, num_points)
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    x_grid = sphere_radius * np.sin(phi_grid) * np.cos(theta_grid)
    y_grid = sphere_radius * np.sin(phi_grid) * np.sin(theta_grid)
    z_grid = sphere_radius * np.cos(phi_grid)

    wormhole_radius = df_decks[outer_radius_netto_label].iloc[0]
    wormhole_height = df_decks[length_outer_radius_netto_label].iloc[0] / 2

    z_cylinder = np.linspace(-wormhole_height, wormhole_height, num_points)
    theta_cyl, z_cyl_grid = np.meshgrid(theta, z_cylinder)
    x_cyl_grid = wormhole_radius * np.cos(theta_cyl)
    y_cyl_grid = wormhole_radius * np.sin(theta_cyl)

    base_radius = wormhole_radius * 1.2
    base_thickness = 2.0

    z_base_ring_top = np.linspace(
        wormhole_height, wormhole_height + base_thickness, num_points
    )
    theta_base_ring, z_base_ring_top_grid = np.meshgrid(theta, z_base_ring_top)
    x_base_ring_top = base_radius * np.cos(theta_base_ring)
    y_base_ring_top = base_radius * np.sin(theta_base_ring)

    z_base_ring_bottom = np.linspace(
        -wormhole_height - base_thickness, -wormhole_height, num_points
    )
    theta_base_ring, z_base_ring_bottom_grid = np.meshgrid(theta, z_base_ring_bottom)
    x_base_ring_bottom = base_radius * np.cos(theta_base_ring)
    y_base_ring_bottom = base_radius * np.sin(theta_base_ring)

    mask_opening = (np.abs(z_grid) >= wormhole_height) & (
        np.sqrt(x_grid**2 + y_grid**2) <= wormhole_radius
    )
    x_grid = np.where(mask_opening, np.nan, x_grid)
    y_grid = np.where(mask_opening, np.nan, y_grid)
    z_grid = np.where(mask_opening, np.nan, z_grid)

    return (
        x_grid,
        y_grid,
        z_grid,
        x_cyl_grid,
        y_cyl_grid,
        z_cyl_grid,
        x_base_ring_top,
        y_base_ring_top,
        z_base_ring_top_grid,
        x_base_ring_bottom,
        y_base_ring_bottom,
        z_base_ring_bottom_grid,
    )
