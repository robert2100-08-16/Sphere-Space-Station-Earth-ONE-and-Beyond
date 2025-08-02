"""Tests for STEP and glTF prototype exporters."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from pathlib import Path

from simulations.sphere_space_station_simulations.adapters.gltf_exporter import (
    export_gltf,
)
from simulations.sphere_space_station_simulations.adapters.step_exporter import (
    export_step,
)
from simulations.sphere_space_station_simulations.data_model import (
    Deck,
    Hull,
    StationModel,
)


def test_exporters_create_files(tmp_path: Path) -> None:
    model = StationModel(decks=[Deck(1, 1.0, 2.0, 3.0)], hull=Hull(10.0))

    step_file = export_step(model, tmp_path / "station.step")
    gltf_file = export_gltf(model, tmp_path / "station.gltf")

    assert step_file.exists()
    assert gltf_file.exists()
    assert "deck 1" in step_file.read_text()
    assert '"deck_count": 1' in gltf_file.read_text()
