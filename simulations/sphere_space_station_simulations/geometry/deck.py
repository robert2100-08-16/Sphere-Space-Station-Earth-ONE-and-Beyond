import logging
from pathlib import Path
from typing import Union, List

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

from .. import animation as animation_mod
from .. import reporting as reporting_mod
from .hull import calculate_hull_geometry


log = logging.getLogger("calc")

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
DATA_DIR = RESULTS_DIR / "data"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _resolve_output_path(file_path: str | None) -> str | None:
    if file_path is None:
        return None
    path = Path(file_path)
    if not path.is_absolute():
        if path.suffix.lower() == ".png":
            path = DATA_DIR / path.name
        else:
            path = RESULTS_DIR / path.name
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


class SphereDeckCalculator:
    DECK_ID_LABEL = "deck_id"
    DECK_NAME = "Deck_"  # Deck name prefix
    INNER_RADIUS_LABEL = "inner_radius_m"
    OUTER_RADIUS_LABEL = "outer_radius_m"
    OUTER_RADIUS_NETTO_LABEL = "outer_radius_netto_m"
    CEILING_THICKNESS_LABEL = "ceiling_thickness_m"
    DECK_HEIGHT_LABEL = "deck_height_m"
    DECK_HEIGHT_NETTO_LABEL = "deck_inner_height_m"
    LENGTH_INNER_RADIUS_LABEL = "length_inner_radius_m"
    LENGTH_OUTER_RADIUS_LABEL = "length_outer_radius_m"
    LENGTH_OUTER_RADIUS_NETTO_LABEL = "length_outer_radius_netto_m"
    BASE_AREA_INNER_RADIUS_LABEL = "base_area_inner_radius_m2"
    BASE_AREA_OUTER_RADIUS_LABEL = "base_area_outer_radius_m2"
    EFFECTIVE_VOLUME_LABEL = "effective_volume_m3"
    NET_ROOM_VOLUME_LABEL = "net_room_volume_m3"
    ROTATION_VELOCITY_LABEL = "rotation_velocity_mps"
    CENTRIFUGAL_ACCELERATION_LABEL = "centrifugal_acceleration_mps2"

    def __init__(
        self,
        title: str,
        sphere_diameter: float,
        hull_thickness: float,
        windows_per_deck_ratio: float,
        num_decks: int,
        deck_000_outer_radius: float,
        deck_height_brutto: float,
        deck_ceiling_thickness: float,
    ):
        """Generate deck dimensions of a sphere.

        Args:
            title (str): The title of the deck calculation.
            sphere_diameter (float): The diameter of the sphere.
            hull_thickness (float): The thickness of the hull.
            windows_per_deck_ratio (float): The ratio of windows per deck.
            num_decks (int): The number of decks.
            deck_000_outer_radius (float): The outer radius of the first deck.
            deck_height_brutto (float): The height of the deck.
            deck_ceiling_thickness (float): The thickness of the deck ceiling.
        """
        self.title = title
        self.sphere_diameter = sphere_diameter
        self.hull_thickness = hull_thickness
        self.windows_per_deck_ratio = windows_per_deck_ratio
        self.inner_sphere_diameter = sphere_diameter - 2 * hull_thickness
        self.num_decks = num_decks
        self.deck_000_outer_radius = deck_000_outer_radius
        self.deck_height_brutto = deck_height_brutto
        self.deck_ceiling_thickness = deck_ceiling_thickness
        log.info("Deck calculator initialized: %s", title)
        self.df_decks = self._calculate_cylindric_decks_of_a_sphere()
        self.hull_geometry = calculate_hull_geometry(
            self.inner_sphere_diameter,
            self.df_decks,
            self.OUTER_RADIUS_NETTO_LABEL,
            self.LENGTH_OUTER_RADIUS_NETTO_LABEL,
        )
        self.window_geometry = self._calculate_window_geometry()
        self.animation_writers = animation.writers.list()
        self.selected_animation_writer = None

    def _calculate_window_geometry(self):
        """Calculate the geometry of windows for each deck and store in a dictionary."""
        window_geometry = {}  # Dictionary to store window coordinates for each deck

        for i in range(1, 13):  # Only for decks 001 to 012
            r = self.df_decks[self.OUTER_RADIUS_LABEL].iloc[i]
            circumference = 2 * np.pi * r  # Calculate the circumference of the deck
            num_windows = max(
                1, int(circumference * self.windows_per_deck_ratio)
            )  # Calculate number of windows

            z_deck_center = (
                self.df_decks[self.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2
            )  # Deck center height
            theta = np.linspace(
                0, 2 * np.pi, num_windows
            )  # Theta values for window positions

            # Calculate window coordinates for the given deck
            x_windows = r * np.cos(theta)  # X-coordinates on the sphere
            y_windows = r * np.sin(theta)  # Y-coordinates on the sphere
            z_windows = np.full(
                num_windows, z_deck_center
            )  # Z-coordinates for upper hemisphere
            z_windows_negative = np.full(
                num_windows, -z_deck_center
            )  # Z-coordinates for lower hemisphere

            # Store the coordinates in the dictionary
            window_geometry[f"{SphereDeckCalculator.DECK_NAME}{i:03}"] = {
                "x": x_windows,
                "y": y_windows,
                "z_upper": z_windows,
                "z_lower": z_windows_negative,
            }

        return window_geometry  # Return the dictionary

    def _calculate_cylindric_decks_of_a_sphere(self):
        sphere_radius = self.inner_sphere_diameter / 2
        deck_labels = [f"{self.DECK_NAME}{i:03}" for i in range(self.num_decks)]
        inner_radius = []
        outer_radius = []
        outer_radius_netto = []
        cylinder_length_inner = []
        cylinder_length_outer = []
        cylinder_length_netto = []
        base_area_inner = []
        base_area_outer = []
        effective_volumes = []
        net_room_volumes = []
        deck_height = []
        deck_height_netto = []

        r0 = 0.0
        r1 = self.deck_000_outer_radius
        for i in range(self.num_decks):
            if i == 0:
                r0 = 0.0
                r1 = self.deck_000_outer_radius
            else:
                r0 = r1
                r1 = r0 + self.deck_height_brutto

            r_medium = r0 + (r1 - r0) / 2
            r_netto = r1 - self.deck_ceiling_thickness

            c_inner = 2 * np.pi * r0
            c_outer = 2 * np.pi * r1
            c_netto = 2 * np.pi * r_netto

            l_inner = (
                2 * np.sqrt(sphere_radius**2 - r0**2) if r0 <= sphere_radius else 0
            )
            l_outer = (
                2 * np.sqrt(sphere_radius**2 - r1**2) if r1 <= sphere_radius else 0
            )
            l_medium = (l_outer + l_inner) / 2
            l_netto = (
                2 * np.sqrt(sphere_radius**2 - r_netto**2)
                if r_netto <= sphere_radius
                else 0
            )
            l_ceiling_medium = (l_outer + l_netto) / 2

            A_inner = c_inner * l_inner
            A_outer = c_outer * l_outer

            A_inner_cross_sectional = np.pi * r0**2
            A_outer_cross_sectional = np.pi * r1**2
            A_netto_cross_sectional = np.pi * r_netto**2

            V_eff = (A_outer_cross_sectional - A_inner_cross_sectional) * l_medium

            V_ceiling = (
                A_outer_cross_sectional - A_netto_cross_sectional
            ) * l_ceiling_medium
            V_net_room = V_eff - V_ceiling

            height = r1 - r0
            height_netto = r_netto - r0

            inner_radius.append(r0)
            outer_radius.append(r1)
            outer_radius_netto.append(r_netto)
            cylinder_length_inner.append(l_inner)
            cylinder_length_outer.append(l_outer)
            cylinder_length_netto.append(l_netto)
            base_area_inner.append(A_inner)
            base_area_outer.append(A_outer)
            effective_volumes.append(V_eff)
            net_room_volumes.append(V_net_room)
            deck_height.append(height)
            deck_height_netto.append(height_netto)

        df_decks = pd.DataFrame(
            {
                self.DECK_ID_LABEL: deck_labels,
                self.INNER_RADIUS_LABEL: inner_radius,
                self.OUTER_RADIUS_LABEL: outer_radius,
                self.OUTER_RADIUS_NETTO_LABEL: outer_radius_netto,
                self.CEILING_THICKNESS_LABEL: [self.deck_ceiling_thickness]
                * self.num_decks,
                self.DECK_HEIGHT_LABEL: deck_height,
                self.DECK_HEIGHT_NETTO_LABEL: deck_height_netto,
                self.LENGTH_INNER_RADIUS_LABEL: cylinder_length_inner,
                self.LENGTH_OUTER_RADIUS_LABEL: cylinder_length_outer,
                self.LENGTH_OUTER_RADIUS_NETTO_LABEL: cylinder_length_netto,
                self.BASE_AREA_INNER_RADIUS_LABEL: base_area_inner,
                self.BASE_AREA_OUTER_RADIUS_LABEL: base_area_outer,
                self.EFFECTIVE_VOLUME_LABEL: effective_volumes,
                self.NET_ROOM_VOLUME_LABEL: net_room_volumes,
            }
        )

        return df_decks

    def calculate_dynamics_of_a_sphere(self, angular_velocity: float):
        log.info("Calculating dynamics with angular velocity %.2f", angular_velocity)
        self.df_decks[self.ROTATION_VELOCITY_LABEL] = (
            self.df_decks[self.OUTER_RADIUS_NETTO_LABEL] * angular_velocity
        )
        self.df_decks[self.CENTRIFUGAL_ACCELERATION_LABEL] = (
            self.df_decks[self.ROTATION_VELOCITY_LABEL] ** 2
            / self.df_decks[self.OUTER_RADIUS_NETTO_LABEL]
        )
        return self.df_decks

    def calculate_total_volume(self):
        return self.df_decks[self.NET_ROOM_VOLUME_LABEL].sum()

    def calculate_total_volume_pressured(self):
        return (
            self.df_decks[self.NET_ROOM_VOLUME_LABEL].sum()
            - self.df_decks[self.NET_ROOM_VOLUME_LABEL].iloc[0]
        )

    # reporting helpers
    def to_string(self, file_path: str | None = None):
        return reporting_mod.deck.to_string(self, file_path)

    def to_html(self, file_path: str | None = None):
        return reporting_mod.deck.to_html(self, file_path)

    def to_csv(self, file_path: str | None = None):
        return reporting_mod.deck.to_csv(self, file_path)

    # animation helpers
    def to_3D_animation_show_all_decks(
        self, file_path: str | None = None, draw_hull: bool = False
    ):
        return animation_mod.deck.to_3D_animation_show_all_decks(
            self, file_path, draw_hull
        )

    def to_3D_animation_rotate_all_decks(
        self,
        file_path: str | None = None,
        frames: int = 25,
        frames_per_second: int = 25,
    ):
        return animation_mod.deck.to_3D_animation_rotate_all_decks(
            self, file_path, frames, frames_per_second
        )

    def to_3D_animation_rotate_hull(
        self,
        file_path: str | None = None,
        frames: int = 25,
        frames_per_second: int = 25,
    ):
        return animation_mod.deck.to_3D_animation_rotate_hull(
            self, file_path, frames, frames_per_second
        )

    def to_3D_animation_rotate_hull_with_windows(
        self,
        file_path: str | None = None,
        frames: int = 25,
        frames_per_second: int = 25,
        rotation_axis: Union[str, List[float]] = "Z",
    ):
        return animation_mod.deck.to_3D_animation_rotate_hull_with_windows(
            self, file_path, frames, frames_per_second, rotation_axis
        )

    def to_3D_animation_rotate_hull_with_gravity_zones(
        self,
        file_path: str | None = None,
        frames: int = 25,
        frames_per_second: int = 25,
        rotation_axis: Union[str, List[float]] = "Z",
        show_gravity_zones: bool = True,
        deck: List[int] | None = None,
    ):
        return animation_mod.deck.to_3D_animation_rotate_hull_with_gravity_zones(
            self,
            file_path,
            frames,
            frames_per_second,
            rotation_axis,
            show_gravity_zones,
            deck,
        )
