"""Tests for prototype geometry exporters."""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pathlib import Path

from simulations.sphere_space_station_simulations.adapters.gltf_exporter import (
    export_gltf,
)
from simulations.sphere_space_station_simulations.adapters.step_exporter import (
    export_step,
)
from simulations.sphere_space_station_simulations.adapters.json_exporter import (
    export_json,
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
    json_file = export_json(model, tmp_path / "station.json")

    assert step_file.exists() and step_file.stat().st_size > 0
    assert gltf_file.exists()
    assert json_file.exists()

    gltf = GLTF2().load(str(gltf_file))
    assert gltf.meshes and gltf.animations

    with json_file.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    assert data["decks"][0]["windows"][0]["size_m"] == 0.2
    assert data["hull"]["windows"][0]["position"][2] == 3.0


def test_step_file_contains_component_counts(tmp_path: Path) -> None:
    model = StationModel(decks=[Deck(1, 1.0, 2.0, 0.5)], hull=Hull(3.0))
    step_file = export_step(model, tmp_path / "station.step")
    with step_file.open("r", encoding="utf-8") as handle:
        content = handle.read()
    assert f"decks={len(model.decks)}" in content
    assert "hull=1" in content
    assert "wormhole=0" in content
