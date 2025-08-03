from simulations.sphere_space_station_simulations import SphereDeckCalculator


def test_deck_dataframe_shape():
    calc = SphereDeckCalculator(
        title="test",
        sphere_diameter=50.0,
        hull_thickness=0.5,
        windows_per_deck_ratio=0.2,
        num_decks=16,
        deck_000_outer_radius=5.0,
        deck_height_brutto=3.0,
        deck_ceiling_thickness=0.5,
    )
    df = calc.df_decks
    assert len(df) == calc.num_decks
    assert (df[calc.OUTER_RADIUS_LABEL] >= df[calc.INNER_RADIUS_LABEL]).all()
    assert (df[calc.NET_ROOM_VOLUME_LABEL] >= 0).all()
