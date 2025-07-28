import pandas as pd
import numpy as np
from pandas import DataFrame
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
from typing import Union, List
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm


class SphereDeckCalculator:
    DECK_LABEL = "Deck"
    DECK_NAME = "Deck_"  # Deck name prefix
    INNER_RADIUS_LABEL = "Inner Radius (m)"
    OUTER_RADIUS_LABEL = "Outer Radius (m)"
    OUTER_RADIUS_NETTO_LABEL = "Outer Radius netto (m)"
    CEILING_THICKNESS_LABEL = "Ceiling Thickness (m)"
    DECK_HEIGHT_LABEL = "Deck Height (m)"
    DECK_HEIGHT_NETTO_LABEL = "Deck Height netto (m)"
    LENGTH_INNER_RADIUS_LABEL = "Length at Inner Radius (m)"
    LENGTH_OUTER_RADIUS_LABEL = "Length at Outer Radius (m)"
    LENGTH_OUTER_RADIUS_NETTO_LABEL = "Length at Outer Radius netto (m)"
    BASE_AREA_INNER_RADIUS_LABEL = "Base Area at Inner Radius (m²)"
    BASE_AREA_OUTER_RADIUS_LABEL = "Base Area at Outer Radius (m²)"
    EFFECTIVE_VOLUME_LABEL = "Effective Volume (m³)"
    NET_ROOM_VOLUME_LABEL = "Net Room Volume (m³)"
    ROTATION_VELOCITY_LABEL = "Rotation Velocity @ radius netto (m/s)"
    CENTRIFUGAL_ACCELERATION_LABEL = "Centrifugal Acceleration @ radius netto (m/s²)"

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
        self.df_decks = self._calculate_cylindric_decks_of_a_sphere()
        self.hull_geometry = self._calculate_hull_geometry()
        self.window_geometry = self._calculate_window_geometry()
        self.animation_writers = animation.writers.list()
        self.selected_animation_writer = None

    def _calculate_hull_geometry(self, num_points: int = 100):
        # Basis-Kugelgeometrie
        sphere_radius = self.inner_sphere_diameter / 2
        theta = np.linspace(0, 2 * np.pi, num_points)
        phi = np.linspace(0, np.pi, num_points)
        theta_grid, phi_grid = np.meshgrid(theta, phi)
        x_grid = sphere_radius * np.sin(phi_grid) * np.cos(theta_grid)
        y_grid = sphere_radius * np.sin(phi_grid) * np.sin(theta_grid)
        z_grid = sphere_radius * np.cos(phi_grid)

        # Durchgangszylinder (Wurmloch) in der Mitte
        wormhole_radius = self.df_decks[self.OUTER_RADIUS_NETTO_LABEL].iloc[0]
        wormhole_height = (
            self.df_decks[self.LENGTH_OUTER_RADIUS_NETTO_LABEL].iloc[0] / 2
        )

        z_cylinder = np.linspace(-wormhole_height, wormhole_height, num_points)
        theta_cylinder, z_cylinder_grid = np.meshgrid(theta, z_cylinder)
        x_cylinder_grid = wormhole_radius * np.cos(theta_cylinder)
        y_cylinder_grid = wormhole_radius * np.sin(theta_cylinder)

        # Sockelringkonstruktion (oben und unten)
        base_radius = (
            wormhole_radius * 1.2
        )  # Sockelradius etwas größer als der Zylinderradius
        base_thickness = 2.0  # Dicke des Sockelrings

        # Oberer Sockelring
        z_base_ring_top = np.linspace(
            wormhole_height, wormhole_height + base_thickness, num_points
        )
        theta_base_ring, z_base_ring_top_grid = np.meshgrid(theta, z_base_ring_top)
        x_base_ring_top = base_radius * np.cos(theta_base_ring)
        y_base_ring_top = base_radius * np.sin(theta_base_ring)

        # Unterer Sockelring
        z_base_ring_bottom = np.linspace(
            -wormhole_height - base_thickness, -wormhole_height, num_points
        )
        theta_base_ring, z_base_ring_bottom_grid = np.meshgrid(
            theta, z_base_ring_bottom
        )
        x_base_ring_bottom = base_radius * np.cos(theta_base_ring)
        y_base_ring_bottom = base_radius * np.sin(theta_base_ring)

        # Filter for excluding the wormhole openings in the hull
        mask_opening = (np.abs(z_grid) >= wormhole_height) & (
            np.sqrt(x_grid**2 + y_grid**2) <= wormhole_radius
        )

        # Apply the mask to hide the hull at the wormhole openings
        x_grid = np.where(mask_opening, np.nan, x_grid)
        y_grid = np.where(mask_opening, np.nan, y_grid)
        z_grid = np.where(mask_opening, np.nan, z_grid)

        return (
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
        )

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
        deck_labels = [f"{self.DECK_LABEL} {i:03}" for i in range(self.num_decks)]
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
                self.DECK_LABEL: deck_labels,
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

    def to_string(self, file_path: str = None):
        string_title = f"{self.title}\n"
        string_table = self.df_decks.to_string()
        string_total_volume = (
            f"Total Volume: {self.calculate_total_volume_pressured()} m³\n"
        )
        string_doc = string_title + "\n" + string_table + "\n" + string_total_volume
        if file_path is not None:
            with open(file_path, "w") as f:
                f.write(string_doc)
            print(
                f"Deck dimensions have been successfully calculated and saved as text in {file_path}."
            )
        return string_doc

    def to_html(self, file_path: str = None):
        html_title = f"<h1>{self.title}</h1>"
        html_table = self.df_decks.to_html()
        html_total_volume = (
            f"<h2>Total Volume: {self.calculate_total_volume_pressured()} m³</h2>"
        )
        html_doc = html_title + html_table + html_total_volume
        if file_path is not None:
            with open(file_path, "w") as f:
                f.write(html_doc)
            print(
                f"Deck dimensions have been successfully calculated and saved as HTML in {file_path}."
            )
        return html_doc

    def to_csv(self, file_path: str = None):
        csv_title = f"{self.title}\n"
        csv_table = self.df_decks.to_csv()
        csv_total_volume = (
            f"Total Volume: {self.calculate_total_volume_pressured()} m³\n"
        )
        csv_doc = csv_title + csv_table + csv_total_volume
        if file_path is not None:
            with open(file_path, "w") as f:
                f.write(csv_doc)
            print(
                f"Deck dimensions have been successfully calculated and saved as CSV in {file_path}."
            )
        return csv_doc

    def _setup_3D_plot(self, ax: Axes3D, title: str, limit: float = None):
        """Setup 3D plot.

        Args:
            ax (_type_): The axes object.
            title (str): The title of the plot.
            limit (float, optional): The limit of the plot. Defaults to None (--> sphere diameter).
        """
        if limit is None:
            limit = self.sphere_diameter / 2
        ax.clear()
        ax.set_xlim([-limit, limit])
        ax.set_ylim([-limit, limit])
        ax.set_zlim([-limit, limit])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title(title)

    def _save_3D_animation(
        self, ani: animation.Animation, file_path: str, frames_per_second: int
    ):
        """Save 3D animation to a file.
            get the best fit writer (gif, mp4, etc. --> pillow, ffmpeg, etc.) (html5, jshtml, etc. --> html) (default --> first available)

        Args:
            ani (animation.Animation): The animation object.
            file_path (str): The file path to save the animation.
            frames_per_second (int): The frames per second of the animation.
        Returns:
            animation.Animation: The animation object.
        """
        if ani.event_source is None:
            print(f"Error: event_source is None for {file_path}")
        else:
            ani.event_source.add_callback(ani._step)
        if file_path is not None:
            # get the best fit writer (gif, mp4, etc. --> pillow, ffmpeg, etc.) (html5, jshtml, etc. --> html) (default --> first available)
            # get the file extension from the file path
            file_extension = file_path.split(".")[-1]
            # get the best fit writer for the file extension
            self.selected_animation_writer = (
                file_extension
                if file_extension in self.animation_writers
                else self.animation_writers[0]
            )
            ani.save(
                file_path, writer=self.selected_animation_writer, fps=frames_per_second
            )
            print(f"\r3D animation has been successfully saved as {file_path}.")
        else:
            print("\r3D animation has been successfully rendered and not be saved.")
        return ani

    def to_3D_animation_show_all_decks(
        self, file_path: str = None, draw_hull: bool = False
    ):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        frames = self.num_decks
        progress_bar = tqdm(total=frames, desc="Rendering Animation")

        def update(num, data, line):
            self._setup_3D_plot(ax, f"{SphereDeckCalculator.DECK_LABEL} {num:03}")
            for i in range(num + 1):
                r = self.df_decks[self.OUTER_RADIUS_LABEL].iloc[i]
                z = np.linspace(
                    -self.df_decks[self.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                    self.df_decks[self.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                    100,
                )
                theta = np.linspace(0, 2 * np.pi, 100)
                theta_grid, z_grid = np.meshgrid(theta, z)
                x_grid = r * np.cos(theta_grid)
                y_grid = r * np.sin(theta_grid)
                ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3)
            progress_bar.update(1)

        ani = FuncAnimation(
            fig, update, frames=frames, fargs=(None, None), repeat=False
        )
        self._save_3D_animation(ani, file_path, frames_per_second=1)
        plt.close(fig)
        progress_bar.close()
        return ani

    def to_3D_animation_rotate_all_decks(
        self, file_path: str = None, frames: int = 25, frames_per_second: int = 25
    ):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        progress_bar = tqdm(total=frames, desc="Rendering Animation")

        def update(num):
            angle = 2 * np.pi * num / frames  # Complete rotation over all frames
            self._setup_3D_plot(
                ax, f"Frame {num}/{frames}, Angle {(angle/np.pi*180.0):.2f} °"
            )
            for i in range(self.num_decks):
                r = self.df_decks[self.OUTER_RADIUS_LABEL].iloc[i]
                z = np.linspace(
                    -self.df_decks[self.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                    self.df_decks[self.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                    100,
                )
                theta = np.linspace(0, 2 * np.pi, 100)
                theta_grid, z_grid = np.meshgrid(theta, z)
                x_grid = r * np.cos(theta_grid + angle)  # Apply rotation
                y_grid = r * np.sin(theta_grid + angle)  # Apply rotation
                color_value = (
                    r / self.inner_sphere_diameter
                )  # Normalize radius to [0, 1]
                ax.plot_surface(
                    x_grid, y_grid, z_grid, alpha=0.3, color=plt.cm.viridis(color_value)
                )
            progress_bar.update(1)  # Update once per frame

        ani = FuncAnimation(fig, update, frames=frames, repeat=False)
        self._save_3D_animation(ani, file_path, frames_per_second)
        plt.close(fig)
        progress_bar.close()
        return ani

    def to_3D_animation_rotate_hull(
        self, file_path: str = None, frames: int = 25, frames_per_second: int = 25
    ):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        progress_bar = tqdm(total=frames, desc="Rendering Animation")

        def update(num):
            angle = 2 * np.pi * num / frames
            self._setup_3D_plot(
                ax, f"Frame {num}/{frames}, Angle {(angle/np.pi*180.0):.2f} °"
            )

            # Load hull geometry
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
            ) = self.hull_geometry

            # Draw sphere hull
            ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3, color="gray")

            # Draw wormhole cylinder
            ax.plot_surface(
                x_cylinder_grid,
                y_cylinder_grid,
                z_cylinder_grid,
                alpha=0.3,
                color="red",
            )

            # Draw top base ring
            ax.plot_surface(
                x_base_ring_top,
                y_base_ring_top,
                z_base_ring_top_grid,
                alpha=0.3,
                color="orange",
            )

            # Draw bottom base ring
            ax.plot_surface(
                x_base_ring_bottom,
                y_base_ring_bottom,
                z_base_ring_bottom_grid,
                alpha=0.3,
                color="orange",
            )

            progress_bar.update(1)

        ani = FuncAnimation(fig, update, frames=frames, repeat=False)
        self._save_3D_animation(ani, file_path, frames_per_second)
        plt.close(fig)
        progress_bar.close()
        return ani

    def _rotation_matrix(axis, theta):
        """Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians."""
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
        """Apply rotation matrix to x, y, z coordinates."""
        xyz = np.vstack([x.flatten(), y.flatten(), z.flatten()])
        rotated_xyz = np.dot(matrix, xyz)
        return (
            rotated_xyz[0].reshape(x.shape),
            rotated_xyz[1].reshape(y.shape),
            rotated_xyz[2].reshape(z.shape),
        )

    def _parse_rotation_axis(rotation_axis: Union[str, List[float]]):
        """Parse rotation axis from string or list."""
        # Determine rotation axis
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
            raise ValueError(
                "rotation_axis must be a string or a list of three floats."
            )
        return axis

    def to_3D_animation_rotate_hull_with_windows(
        self,
        file_path: str = None,
        frames: int = 25,
        frames_per_second: int = 25,
        rotation_axis: Union[str, List[float]] = "Z",
    ):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        progress_bar = tqdm(total=frames, desc="Rendering Animation")
        axis = SphereDeckCalculator._parse_rotation_axis(rotation_axis)

        def update(num):
            angle = 2 * np.pi * num / frames  # Complete rotation over all frames
            rot_matrix = SphereDeckCalculator._rotation_matrix(
                axis, angle
            )  # Calculate rotation matrix

            self._setup_3D_plot(
                ax, f"Frame {num}/{frames}, Angle {(angle/np.pi*180.0):.2f} °"
            )

            # Load hull geometry
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
            ) = self.hull_geometry

            # Apply rotation to hull
            x_grid, y_grid, z_grid = SphereDeckCalculator._apply_rotation(
                rot_matrix, x_grid, y_grid, z_grid
            )

            # Apply rotation to wormhole cylinder
            x_cylinder_grid, y_cylinder_grid, z_cylinder_grid = (
                SphereDeckCalculator._apply_rotation(
                    rot_matrix, x_cylinder_grid, y_cylinder_grid, z_cylinder_grid
                )
            )

            # Apply rotation to right base ring
            x_base_ring_top, y_base_ring_top, z_base_ring_top_grid = (
                SphereDeckCalculator._apply_rotation(
                    rot_matrix, x_base_ring_top, y_base_ring_top, z_base_ring_top_grid
                )
            )

            # Apply rotation to left base ring
            x_base_ring_bottom, y_base_ring_bottom, z_base_ring_bottom_grid = (
                SphereDeckCalculator._apply_rotation(
                    rot_matrix,
                    x_base_ring_bottom,
                    y_base_ring_bottom,
                    z_base_ring_bottom_grid,
                )
            )

            # Draw sphere hull
            ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3, color="green")

            # Draw wormhole cylinder
            ax.plot_surface(
                x_cylinder_grid,
                y_cylinder_grid,
                z_cylinder_grid,
                alpha=0.3,
                color="red",
            )

            # Draw top base ring
            ax.plot_surface(
                x_base_ring_top,
                y_base_ring_top,
                z_base_ring_top_grid,
                alpha=0.3,
                color="orange",
            )

            # Draw bottom base ring
            ax.plot_surface(
                x_base_ring_bottom,
                y_base_ring_bottom,
                z_base_ring_bottom_grid,
                alpha=0.3,
                color="orange",
            )

            # Apply rotation to windows and draw them
            for deck, coordinates in self.window_geometry.items():
                x_windows = coordinates["x"]
                y_windows = coordinates["y"]
                z_upper = coordinates["z_upper"]
                z_lower = coordinates["z_lower"]

                # Apply rotation to windows
                x_rot_upper, y_rot_upper, z_rot_upper = (
                    SphereDeckCalculator._apply_rotation(
                        rot_matrix, x_windows, y_windows, z_upper
                    )
                )
                x_rot_lower, y_rot_lower, z_rot_lower = (
                    SphereDeckCalculator._apply_rotation(
                        rot_matrix, x_windows, y_windows, z_lower
                    )
                )

                # Plot upper hemisphere windows
                ax.scatter(x_rot_upper, y_rot_upper, z_rot_upper, color="blue", s=1)
                # Plot lower hemisphere windows
                ax.scatter(x_rot_lower, y_rot_lower, z_rot_lower, color="blue", s=1)

            progress_bar.update(1)  # Update once per frame

        ani = FuncAnimation(fig, update, frames=frames, repeat=False)
        self._save_3D_animation(ani, file_path, frames_per_second)
        plt.close(fig)
        progress_bar.close()
        return ani

    def to_3D_animation_rotate_hull_with_gravity_zones(
        self,
        file_path: str = None,
        frames: int = 25,
        frames_per_second: int = 25,
        rotation_axis: Union[str, List[float]] = "Z",
        show_gravity_zones: bool = True,
        deck: List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    ):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        progress_bar = tqdm(total=frames, desc="Rendering Animation")
        axis = SphereDeckCalculator._parse_rotation_axis(rotation_axis)

        def update(num):
            angle = 2 * np.pi * num / frames  # Complete rotation over all frames
            rot_matrix = SphereDeckCalculator._rotation_matrix(
                axis, angle
            )  # Rotation matrix

            self._setup_3D_plot(
                ax, f"Frame {num}/{frames}, Angle {(angle/np.pi*180.0):.2f} °"
            )

            # Load hull geometry
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
            ) = self.hull_geometry

            # Apply rotation to hull
            x_grid, y_grid, z_grid = SphereDeckCalculator._apply_rotation(
                rot_matrix, x_grid, y_grid, z_grid
            )

            # Apply rotation to wormhole cylinder
            x_cylinder_grid, y_cylinder_grid, z_cylinder_grid = (
                SphereDeckCalculator._apply_rotation(
                    rot_matrix, x_cylinder_grid, y_cylinder_grid, z_cylinder_grid
                )
            )

            # Apply rotation to right base ring
            x_base_ring_top, y_base_ring_top, z_base_ring_top_grid = (
                SphereDeckCalculator._apply_rotation(
                    rot_matrix, x_base_ring_top, y_base_ring_top, z_base_ring_top_grid
                )
            )

            # Apply rotation to left base ring
            x_base_ring_bottom, y_base_ring_bottom, z_base_ring_bottom_grid = (
                SphereDeckCalculator._apply_rotation(
                    rot_matrix,
                    x_base_ring_bottom,
                    y_base_ring_bottom,
                    z_base_ring_bottom_grid,
                )
            )

            # Draw sphere hull
            ax.plot_surface(x_grid, y_grid, z_grid, alpha=0, color="white")

            # Draw wormhole cylinder
            ax.plot_surface(
                x_cylinder_grid,
                y_cylinder_grid,
                z_cylinder_grid,
                alpha=1,
                color="yellow",
            )

            # Draw top base ring
            ax.plot_surface(
                x_base_ring_top,
                y_base_ring_top,
                z_base_ring_top_grid,
                alpha=1,
                color="orange",
            )

            # Draw bottom base ring
            ax.plot_surface(
                x_base_ring_bottom,
                y_base_ring_bottom,
                z_base_ring_bottom_grid,
                alpha=1,
                color="orange",
            )

            window_depth = self.hull_thickness
            # Draw gravity zones and windows for the selected decks
            for i in deck:
                r = self.df_decks[self.OUTER_RADIUS_LABEL].iloc[i]
                z = np.linspace(
                    -self.df_decks[self.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                    self.df_decks[self.LENGTH_OUTER_RADIUS_LABEL].iloc[i] / 2,
                    100,
                )
                theta = np.linspace(0, 2 * np.pi, 100)
                theta_grid, z_grid = np.meshgrid(theta, z)
                x_grid = r * np.cos(theta_grid)
                y_grid = r * np.sin(theta_grid)

                deck_color = "green"  # Default deck color
                if show_gravity_zones:
                    # Get the centrifugal acceleration to determine color
                    centrifugal_acceleration = self.df_decks[
                        self.CENTRIFUGAL_ACCELERATION_LABEL
                    ].iloc[i]
                    # Normalize acceleration between 0 and max for color mapping
                    color_value = (
                        centrifugal_acceleration / 9.81
                    )  # Normalize to 1g (green)
                    deck_color = plt.cm.jet(color_value)  # Color mapping
                # Plot the deck
                ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3, color=deck_color)

                # Draw windows for each selected deck
                deck_key = f"{SphereDeckCalculator.DECK_NAME}{i:03}"
                if deck_key in self.window_geometry:
                    coordinates = self.window_geometry[deck_key]
                    x_windows = coordinates["x"]
                    y_windows = coordinates["y"]
                    z_upper = coordinates["z_upper"]
                    z_lower = coordinates["z_lower"]

                    # Apply rotation to windows
                    x_rot_upper, y_rot_upper, z_rot_upper = (
                        SphereDeckCalculator._apply_rotation(
                            rot_matrix, x_windows, y_windows, z_upper
                        )
                    )
                    x_rot_lower, y_rot_lower, z_rot_lower = (
                        SphereDeckCalculator._apply_rotation(
                            rot_matrix, x_windows, y_windows, z_lower
                        )
                    )

                    # For each window, create a small cylinder to represent depth
                    for j in range(len(x_rot_upper)):
                        # Calculate vector for window depth (cylinder along the normal of the sphere)
                        window_vector_x = (
                            x_rot_upper[j] - window_depth * x_rot_upper[j] / r
                        )
                        window_vector_y = (
                            y_rot_upper[j] - window_depth * y_rot_upper[j] / r
                        )
                        window_vector_z = (
                            z_rot_upper[j] - window_depth * z_rot_upper[j] / r
                        )

                        # Create cylinder representing the window depth
                        window_z = np.linspace(z_rot_upper[j], window_vector_z, 10)
                        window_theta = np.linspace(0, 2 * np.pi, 10)
                        window_theta_grid, window_z_grid = np.meshgrid(
                            window_theta, window_z
                        )
                        window_x_grid = (r - window_depth) * np.cos(window_theta_grid)
                        window_y_grid = (r - window_depth) * np.sin(window_theta_grid)

                        # Plot cylindrical window
                        ax.plot_surface(
                            window_x_grid,
                            window_y_grid,
                            window_z_grid,
                            color="blue",
                            alpha=1,
                        )

            progress_bar.update(1)  # Update progress bar

        ani = FuncAnimation(fig, update, frames=frames, repeat=False)
        self._save_3D_animation(ani, file_path, frames_per_second)
        plt.close(fig)
        progress_bar.close()
        return ani


# Example function call
if __name__ == "__main__":
    calculator = SphereDeckCalculator(
        "Deck Dimensions of a Sphere",
        sphere_diameter=127.0,
        hull_thickness=0.5,
        windows_per_deck_ratio=0.20,
        num_decks=16,
        deck_000_outer_radius=10.5,
        deck_height_brutto=3.5,
        deck_ceiling_thickness=0.5,
    )

    df_decks = calculator.calculate_dynamics_of_a_sphere(angular_velocity=0.5)
    print(calculator.to_string())
    # calculator.to_csv("deck_dimensions.csv")
    # calculator.to_html("deck_dimensions.html")
    # calculator.to_3D_animation_show_all_decks("deck_animation.html")
    # calculator.to_3D_animation_rotate_all_decks("deck_animation_rotate.html")
    # calculator.to_3D_animation_rotate_hull_with_windows(
    #   "hull_with_windows_animation.html",
    #  frames=25,
    # frames_per_second=5,
    # rotation_axis="Z",
    # )
    # calculator.to_3D_animation_rotate_hull("hull_animation.html")
    calculator.to_3D_animation_rotate_hull_with_gravity_zones(
        "hull_with_gravity_zones_animation.html",
        frames=25,
        frames_per_second=25,
        rotation_axis="Z",
        show_gravity_zones=False,
    )
