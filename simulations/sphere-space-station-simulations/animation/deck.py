"""Animation utilities for :class:`SphereDeckCalculator`."""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, Animation
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
from typing import Union, List

from ..geometry import deck as geom_deck


def _setup_3D_plot(
    calc: geom_deck.SphereDeckCalculator,
    ax: Axes3D,
    title: str,
    limit: float | None = None,
):
    if limit is None:
        limit = calc.sphere_diameter / 2
    ax.clear()
    ax.set_xlim([-limit, limit])
    ax.set_ylim([-limit, limit])
    ax.set_zlim([-limit, limit])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(title)


def _save_3D_animation(
    calc: geom_deck.SphereDeckCalculator,
    ani: Animation,
    file_path: str,
    frames_per_second: int,
) -> Animation:
    if ani.event_source is None:
        print(f"Error: event_source is None for {file_path}")
    else:
        ani.event_source.add_callback(ani._step)
    resolved = geom_deck._resolve_output_path(file_path)
    if resolved is not None:
        file_extension = resolved.split(".")[-1]
        calc.selected_animation_writer = (
            file_extension
            if file_extension in calc.animation_writers
            else calc.animation_writers[0]
        )
        ani.save(resolved, writer=calc.selected_animation_writer, fps=frames_per_second)
        print(f"\r3D animation has been successfully saved as {resolved}.")
    else:
        print("\r3D animation has been successfully rendered and not be saved.")
    return ani


def to_3D_animation_show_all_decks(
    calc: geom_deck.SphereDeckCalculator,
    file_path: str | None = None,
    draw_hull: bool = False,
):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    frames = calc.num_decks
    progress_bar = tqdm(total=frames, desc="Rendering Animation")

    def update(num, data, line):
        _setup_3D_plot(calc, ax, f"{geom_deck.SphereDeckCalculator.DECK_NAME}{num:03}")
        for i in range(num + 1):
            r = calc.df_decks[calc.OUTER_RADIUS_LABEL].iloc[i]
            z = np.linspace(
                -calc.df_decks[calc.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                calc.df_decks[calc.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                100,
            )
            theta = np.linspace(0, 2 * np.pi, 100)
            theta_grid, z_grid = np.meshgrid(theta, z)
            x_grid = r * np.cos(theta_grid)
            y_grid = r * np.sin(theta_grid)
            ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3)
        progress_bar.update(1)

    ani = FuncAnimation(fig, update, frames=frames, fargs=(None, None), repeat=False)
    _save_3D_animation(calc, ani, file_path, frames_per_second=1)
    plt.close(fig)
    progress_bar.close()
    return ani


def to_3D_animation_rotate_all_decks(
    calc: geom_deck.SphereDeckCalculator,
    file_path: str | None = None,
    frames: int = 25,
    frames_per_second: int = 25,
):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    progress_bar = tqdm(total=frames, desc="Rendering Animation")

    def update(num):
        angle = 2 * np.pi * num / frames
        _setup_3D_plot(
            calc, ax, f"Frame {num}/{frames}, Angle {(angle/np.pi*180.0):.2f} °"
        )
        for i in range(calc.num_decks):
            r = calc.df_decks[calc.OUTER_RADIUS_LABEL].iloc[i]
            z = np.linspace(
                -calc.df_decks[calc.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                calc.df_decks[calc.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                100,
            )
            theta = np.linspace(0, 2 * np.pi, 100)
            theta_grid, z_grid = np.meshgrid(theta, z)
            x_grid = r * np.cos(theta_grid + angle)
            y_grid = r * np.sin(theta_grid + angle)
            color_value = r / calc.inner_sphere_diameter
            ax.plot_surface(
                x_grid, y_grid, z_grid, alpha=0.3, color=plt.cm.viridis(color_value)
            )
        progress_bar.update(1)

    ani = FuncAnimation(fig, update, frames=frames, repeat=False)
    _save_3D_animation(calc, ani, file_path, frames_per_second)
    plt.close(fig)
    progress_bar.close()
    return ani


def to_3D_animation_rotate_hull(
    calc: geom_deck.SphereDeckCalculator,
    file_path: str | None = None,
    frames: int = 25,
    frames_per_second: int = 25,
):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    progress_bar = tqdm(total=frames, desc="Rendering Animation")

    def update(num):
        angle = 2 * np.pi * num / frames
        _setup_3D_plot(
            calc, ax, f"Frame {num}/{frames}, Angle {(angle/np.pi*180.0):.2f} °"
        )
        (
            x_grid,
            y_grid,
            z_grid,
            x_cylinder_grid,
            y_cylinder_grid,
            z_cylinder_grid,
            x_base_ring_top,
            y_base_ring_top,
            z_base_ring_top_grid,
            x_base_ring_bottom,
            y_base_ring_bottom,
            z_base_ring_bottom_grid,
        ) = calc.hull_geometry
        ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3, color="gray")
        ax.plot_surface(
            x_cylinder_grid, y_cylinder_grid, z_cylinder_grid, alpha=0.3, color="red"
        )
        ax.plot_surface(
            x_base_ring_top,
            y_base_ring_top,
            z_base_ring_top_grid,
            alpha=0.3,
            color="orange",
        )
        ax.plot_surface(
            x_base_ring_bottom,
            y_base_ring_bottom,
            z_base_ring_bottom_grid,
            alpha=0.3,
            color="orange",
        )
        progress_bar.update(1)

    ani = FuncAnimation(fig, update, frames=frames, repeat=False)
    _save_3D_animation(calc, ani, file_path, frames_per_second)
    plt.close(fig)
    progress_bar.close()
    return ani


def _rotation_matrix(axis, theta):
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array(
        [
            [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
            [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
            [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc],
        ]
    )


def _apply_rotation(matrix, x, y, z):
    xyz = np.vstack([x.flatten(), y.flatten(), z.flatten()])
    rotated_xyz = np.dot(matrix, xyz)
    return (
        rotated_xyz[0].reshape(x.shape),
        rotated_xyz[1].reshape(y.shape),
        rotated_xyz[2].reshape(z.shape),
    )


def _parse_rotation_axis(rotation_axis: Union[str, List[float]]):
    axis = np.zeros(3)
    if isinstance(rotation_axis, str):
        if "X" in rotation_axis.upper():
            axis[0] = 1
        if "Y" in rotation_axis.upper():
            axis[1] = 1
        if "Z" in rotation_axis.upper():
            axis[2] = 1
        if not np.any(axis):
            raise ValueError(
                "Invalid rotation axis. Choose from 'X', 'Y', 'Z', or any combination of them."
            )
    elif isinstance(rotation_axis, list) and len(rotation_axis) == 3:
        axis = np.array(rotation_axis)
    else:
        raise ValueError("rotation_axis must be a string or a list of three floats.")
    return axis


def to_3D_animation_rotate_hull_with_windows(
    calc: geom_deck.SphereDeckCalculator,
    file_path: str | None = None,
    frames: int = 25,
    frames_per_second: int = 25,
    rotation_axis: Union[str, List[float]] = "Z",
):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    progress_bar = tqdm(total=frames, desc="Rendering Animation")
    axis = _parse_rotation_axis(rotation_axis)

    def update(num):
        angle = 2 * np.pi * num / frames
        rot_matrix = _rotation_matrix(axis, angle)
        _setup_3D_plot(
            calc, ax, f"Frame {num}/{frames}, Angle {(angle/np.pi*180.0):.2f} °"
        )
        (
            x_grid,
            y_grid,
            z_grid,
            x_cylinder_grid,
            y_cylinder_grid,
            z_cylinder_grid,
            x_base_ring_top,
            y_base_ring_top,
            z_base_ring_top_grid,
            x_base_ring_bottom,
            y_base_ring_bottom,
            z_base_ring_bottom_grid,
        ) = calc.hull_geometry
        x_grid, y_grid, z_grid = _apply_rotation(rot_matrix, x_grid, y_grid, z_grid)
        x_cylinder_grid, y_cylinder_grid, z_cylinder_grid = _apply_rotation(
            rot_matrix, x_cylinder_grid, y_cylinder_grid, z_cylinder_grid
        )
        x_base_ring_top, y_base_ring_top, z_base_ring_top_grid = _apply_rotation(
            rot_matrix, x_base_ring_top, y_base_ring_top, z_base_ring_top_grid
        )
        x_base_ring_bottom, y_base_ring_bottom, z_base_ring_bottom_grid = (
            _apply_rotation(
                rot_matrix,
                x_base_ring_bottom,
                y_base_ring_bottom,
                z_base_ring_bottom_grid,
            )
        )
        ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3, color="green")
        ax.plot_surface(
            x_cylinder_grid, y_cylinder_grid, z_cylinder_grid, alpha=0.3, color="red"
        )
        ax.plot_surface(
            x_base_ring_top,
            y_base_ring_top,
            z_base_ring_top_grid,
            alpha=0.3,
            color="orange",
        )
        ax.plot_surface(
            x_base_ring_bottom,
            y_base_ring_bottom,
            z_base_ring_bottom_grid,
            alpha=0.3,
            color="orange",
        )
        for deck_key, coordinates in calc.window_geometry.items():
            x_windows = coordinates["x"]
            y_windows = coordinates["y"]
            z_upper = coordinates["z_upper"]
            z_lower = coordinates["z_lower"]
            x_rot_upper, y_rot_upper, z_rot_upper = _apply_rotation(
                rot_matrix, x_windows, y_windows, z_upper
            )
            x_rot_lower, y_rot_lower, z_rot_lower = _apply_rotation(
                rot_matrix, x_windows, y_windows, z_lower
            )
            ax.scatter(x_rot_upper, y_rot_upper, z_rot_upper, color="blue", s=1)
            ax.scatter(x_rot_lower, y_rot_lower, z_rot_lower, color="blue", s=1)
        progress_bar.update(1)

    ani = FuncAnimation(fig, update, frames=frames, repeat=False)
    _save_3D_animation(calc, ani, file_path, frames_per_second)
    plt.close(fig)
    progress_bar.close()
    return ani


def to_3D_animation_rotate_hull_with_gravity_zones(
    calc: geom_deck.SphereDeckCalculator,
    file_path: str | None = None,
    frames: int = 25,
    frames_per_second: int = 25,
    rotation_axis: Union[str, List[float]] = "Z",
    show_gravity_zones: bool = True,
    deck: List[int] | None = None,
):
    if deck is None:
        deck = list(range(calc.num_decks))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    progress_bar = tqdm(total=frames, desc="Rendering Animation")
    axis = _parse_rotation_axis(rotation_axis)

    def update(num):
        angle = 2 * np.pi * num / frames
        rot_matrix = _rotation_matrix(axis, angle)
        _setup_3D_plot(
            calc, ax, f"Frame {num}/{frames}, Angle {(angle/np.pi*180.0):.2f} °"
        )
        (
            x_grid,
            y_grid,
            z_grid,
            x_cylinder_grid,
            y_cylinder_grid,
            z_cylinder_grid,
            x_base_ring_top,
            y_base_ring_top,
            z_base_ring_top_grid,
            x_base_ring_bottom,
            y_base_ring_bottom,
            z_base_ring_bottom_grid,
        ) = calc.hull_geometry
        x_grid, y_grid, z_grid = _apply_rotation(rot_matrix, x_grid, y_grid, z_grid)
        x_cylinder_grid, y_cylinder_grid, z_cylinder_grid = _apply_rotation(
            rot_matrix, x_cylinder_grid, y_cylinder_grid, z_cylinder_grid
        )
        x_base_ring_top, y_base_ring_top, z_base_ring_top_grid = _apply_rotation(
            rot_matrix, x_base_ring_top, y_base_ring_top, z_base_ring_top_grid
        )
        x_base_ring_bottom, y_base_ring_bottom, z_base_ring_bottom_grid = (
            _apply_rotation(
                rot_matrix,
                x_base_ring_bottom,
                y_base_ring_bottom,
                z_base_ring_bottom_grid,
            )
        )
        ax.plot_surface(x_grid, y_grid, z_grid, alpha=0, color="white")
        ax.plot_surface(
            x_cylinder_grid, y_cylinder_grid, z_cylinder_grid, alpha=1, color="yellow"
        )
        ax.plot_surface(
            x_base_ring_top,
            y_base_ring_top,
            z_base_ring_top_grid,
            alpha=1,
            color="orange",
        )
        ax.plot_surface(
            x_base_ring_bottom,
            y_base_ring_bottom,
            z_base_ring_bottom_grid,
            alpha=1,
            color="orange",
        )
        window_depth = calc.hull_thickness
        for i in deck:
            r = calc.df_decks[calc.OUTER_RADIUS_LABEL].iloc[i]
            z = np.linspace(
                -calc.df_decks[calc.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                calc.df_decks[calc.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                100,
            )
            theta = np.linspace(0, 2 * np.pi, 100)
            theta_grid, z_grid = np.meshgrid(theta, z)
            x_grid_d = r * np.cos(theta_grid)
            y_grid_d = r * np.sin(theta_grid)
            deck_color = "green"
            if show_gravity_zones:
                centrifugal_acceleration = calc.df_decks[
                    calc.CENTRIFUGAL_ACCELERATION_LABEL
                ].iloc[i]
                color_value = centrifugal_acceleration / 9.81
                deck_color = plt.cm.jet(color_value)
            ax.plot_surface(x_grid_d, y_grid_d, z_grid, alpha=0.3, color=deck_color)
            deck_key = f"{geom_deck.SphereDeckCalculator.DECK_NAME}{i:03}"
            if deck_key in calc.window_geometry:
                coordinates = calc.window_geometry[deck_key]
                x_windows = coordinates["x"]
                y_windows = coordinates["y"]
                z_upper = coordinates["z_upper"]
                z_lower = coordinates["z_lower"]
                x_rot_upper, y_rot_upper, z_rot_upper = _apply_rotation(
                    rot_matrix, x_windows, y_windows, z_upper
                )
                x_rot_lower, y_rot_lower, z_rot_lower = _apply_rotation(
                    rot_matrix, x_windows, y_windows, z_lower
                )
                for j in range(len(x_rot_upper)):
                    window_vector_x = x_rot_upper[j] - window_depth * x_rot_upper[j] / r
                    window_vector_y = y_rot_upper[j] - window_depth * y_rot_upper[j] / r
                    window_vector_z = z_rot_upper[j] - window_depth * z_rot_upper[j] / r
                    window_z = np.linspace(z_rot_upper[j], window_vector_z, 10)
                    window_theta = np.linspace(0, 2 * np.pi, 10)
                    window_theta_grid, window_z_grid = np.meshgrid(
                        window_theta, window_z
                    )
                    window_x_grid = (r - window_depth) * np.cos(window_theta_grid)
                    window_y_grid = (r - window_depth) * np.sin(window_theta_grid)
                    ax.plot_surface(
                        window_x_grid,
                        window_y_grid,
                        window_z_grid,
                        color="blue",
                        alpha=1,
                    )
        progress_bar.update(1)

    ani = FuncAnimation(fig, update, frames=frames, repeat=False)
    _save_3D_animation(calc, ani, file_path, frames_per_second)
    plt.close(fig)
    progress_bar.close()
    return ani
