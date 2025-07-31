import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from simulations.scripts.deck_calculations_script import SphereDeckCalculator


def test_window_count():
    calc = SphereDeckCalculator(
        title="test",
        sphere_diameter=100.0,
        hull_thickness=1.0,
        windows_per_deck_ratio=0.5,
        num_decks=16,
        deck_000_outer_radius=2.0,
        deck_height_brutto=3.0,
        deck_ceiling_thickness=0.5,
    )
    windows = calc.window_geometry
    assert len(windows) > 0
