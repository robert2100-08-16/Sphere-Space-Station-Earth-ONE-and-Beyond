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
    Window,
)
from pygltflib import GLTF2


def test_exporters_create_files(tmp_path: Path) -> None:
    model = StationModel(
        decks=[Deck(1, 1.0, 2.0, 0.5, windows=[Window((0.0, 0.0, 0.0), 0.2)])],
        hull=Hull(3.0, windows=[Window((0.0, 0.0, 3.0), 0.5)]),
    )

    step_file = export_step(model, tmp_path / "station.step")
    gltf_file = export_gltf(model, tmp_path / "station.glb")

    assert step_file.exists() and step_file.stat().st_size > 0
    assert gltf_file.exists()
    gltf = GLTF2().load(str(gltf_file))
    assert gltf.meshes and gltf.animations
