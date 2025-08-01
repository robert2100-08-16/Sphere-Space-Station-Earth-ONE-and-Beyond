import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from simulations.deck_calculator.station_simulation import StationSimulation


def test_models_load():
    sim = StationSimulation(
        enable_docking=False,
        enable_mission_control=False,
        enable_life_support=False,
        enable_emergency_drills=False,
    )
    assert sim.decks is not None
    assert sim.hull is not None
