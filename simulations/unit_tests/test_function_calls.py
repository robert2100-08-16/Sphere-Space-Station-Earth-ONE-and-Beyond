import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulations.sphere_space_station_simulations import SphereDeckCalculator


def create_calculator():
    return SphereDeckCalculator(
        title="test",
        sphere_diameter=50.0,
        hull_thickness=0.5,
        windows_per_deck_ratio=0.2,
        num_decks=16,
        deck_000_outer_radius=5.0,
        deck_height_brutto=3.0,
        deck_ceiling_thickness=0.5,
    )


def test_to_csv_and_html(tmp_path):
    calc = create_calculator()
    csv_path = tmp_path / "deck_dimensions.csv"
    html_path = tmp_path / "deck_dimensions.html"
    calc.to_csv(str(csv_path))
    calc.to_html(str(html_path))
    assert csv_path.exists()
    assert html_path.exists()


def test_animations(tmp_path):
    calc = create_calculator()
    show_all = tmp_path / "deck_animation.html"
    rotate_all = tmp_path / "deck_animation_rotate.html"
    rotate_windows = tmp_path / "hull_with_windows_animation.html"
    rotate_hull = tmp_path / "hull_animation.html"
    rotate_gravity = tmp_path / "hull_with_gravity_zones_animation.html"

    calc.to_3D_animation_show_all_decks(str(show_all))
    calc.to_3D_animation_rotate_all_decks(str(rotate_all), frames=2, frames_per_second=5)
    calc.to_3D_animation_rotate_hull_with_windows(
        str(rotate_windows), frames=2, frames_per_second=5, rotation_axis="Z"
    )
    calc.to_3D_animation_rotate_hull(str(rotate_hull), frames=2, frames_per_second=5)
    calc.to_3D_animation_rotate_hull_with_gravity_zones(
        str(rotate_gravity),
        frames=2,
        frames_per_second=5,
        rotation_axis="Z",
        show_gravity_zones=False,
    )

    assert show_all.exists()
    assert rotate_all.exists()
    assert rotate_windows.exists()
    assert rotate_hull.exists()
    assert rotate_gravity.exists()
