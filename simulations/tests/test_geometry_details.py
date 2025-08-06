from simulations.sphere_space_station_simulations import SphereDeckCalculator


def _create_calc(**kwargs):
    return SphereDeckCalculator(
        title="Test",
        sphere_diameter=100.0,
        hull_thickness=1.0,
        windows_per_deck_ratio=0.01,
        num_decks=16,
        deck_000_outer_radius=2.0,
        deck_height_brutto=3.0,
        deck_ceiling_thickness=0.5,
        **kwargs,
    )


def test_support_geometry_count():
    calc = _create_calc(supports_per_deck=4)
    supports = calc.support_geometry["Deck_001"]
    assert len(supports["x"]) == 4


def test_docking_port_positions():
    calc = _create_calc(num_docking_ports=3)
    ports = calc.docking_ports
    assert len(ports["x"]) == 3
    assert all(z == 0 for z in ports["z"])
