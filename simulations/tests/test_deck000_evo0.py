import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from simulations.sphere_space_station_simulations.evolutions.evolution_00.deck000 import (
    Deck000Params,
    generate_segments,
)


def nearly(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_segment_positions_match_spec_table_1():
    p = Deck000Params()
    segs = generate_segments(p)
    # Expected first items:
    exp = [
        ("clearance_north", 0.0, 3.5),
        ("ring_00", 3.5, 13.5),
        ("window_00", 13.5, 23.5),
        ("ring_01", 23.5, 33.5),
        ("window_01", 33.5, 43.5),
        ("ring_02", 43.5, 53.5),
        ("window_02", 53.5, 63.5),
        ("ring_03", 63.5, 73.5),
        ("window_03", 73.5, 83.5),
        ("ring_04", 83.5, 93.5),
        ("window_04", 93.5, 103.5),
        ("ring_05", 103.5, 113.5),
        ("window_06", 113.5, 123.5),
        ("clearance_south", 123.5, 127.0),
    ]
    names = [s["name"] for s in segs]
    z0s = [s["z0"] for s in segs]
    z1s = [s["z1"] for s in segs]
    assert len(segs) == len(exp)
    for i, (name, z0, z1) in enumerate(exp):
        assert names[i] == name
        assert nearly(z0s[i], z0)
        assert nearly(z1s[i], z1)


def test_radii_are_correct():
    p = Deck000Params()
    segs = generate_segments(p)
    for s in segs:
        if s["type"] == "ring":
            assert math.isclose(s["r_inner"], p.ring_ri)
        else:
            assert math.isclose(s["r_inner"], p.barrel_ri)
        assert math.isclose(s["r_outer"], p.barrel_ro)
