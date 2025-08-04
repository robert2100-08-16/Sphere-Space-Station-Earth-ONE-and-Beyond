"""Extended tests for geometry exporters and Blender import."""

import os
import sys
import json
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pathlib import Path

from pygltflib import GLTF2

from simulations.sphere_space_station_simulations.adapters.gltf_exporter import (
    export_gltf,
)
from simulations.sphere_space_station_simulations.adapters.json_exporter import (
    export_json,
)
from simulations.sphere_space_station_simulations.data_model import (
    Deck,
    Hull,
    StationModel,
    Wormhole,
)
from simulations.blender_hull_simulation import adapter


def _make_model() -> StationModel:
    """Create a simple station model with two decks and a hull."""
    return StationModel(
        decks=[Deck(1, 0.0, 1.0, 0.2), Deck(2, 1.0, 2.0, 0.2)],
        hull=Hull(3.0),
        wormhole=Wormhole(0.5, 1.0),
    )


def test_gltf_contains_all_components(tmp_path: Path) -> None:
    model = _make_model()
    gltf_path = export_gltf(model, tmp_path / "station.glb")
    gltf = GLTF2().load(str(gltf_path))

    # Mesh count should equal decks + hull + optional wormhole
    expected_meshes = (
        len(model.decks) + (1 if model.hull else 0) + (1 if model.wormhole else 0)
    )
    assert len(gltf.meshes) == expected_meshes


def test_json_export_has_all_fields(tmp_path: Path) -> None:
    model = _make_model()
    json_path = export_json(model, tmp_path / "station.json")

    with json_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    expected_deck_fields = {
        "id",
        "inner_radius_m",
        "outer_radius_m",
        "height_m",
        "windows",
        "net_inner_radius_m",
        "net_outer_radius_m",
        "net_height_m",
        "base_area_m2",
        "volume_m3",
    }
    expected_hull_fields = {
        "radius_m",
        "windows",
        "net_radius_m",
        "surface_area_m2",
        "volume_m3",
    }
    assert expected_deck_fields <= set(data["decks"][0].keys())
    assert expected_hull_fields <= set(data["hull"].keys())
    expected_wormhole_fields = {"radius_m", "height_m", "base_thickness_m"}
    assert expected_wormhole_fields <= set(data["wormhole"].keys())


def test_blender_import_mesh_count(monkeypatch, tmp_path: Path) -> None:
    model = _make_model()
    gltf_path = export_gltf(model, tmp_path / "station.glb")

    gltf = GLTF2().load(str(gltf_path))
    expected_meshes = len(gltf.meshes)

    def import_gltf_stub(filepath: str) -> None:
        gltf_local = GLTF2().load(filepath)
        bpy_stub.data.objects = [
            SimpleNamespace(type="MESH", data=SimpleNamespace(materials=[]))
            for _ in gltf_local.meshes
        ]

    bpy_stub = SimpleNamespace(
        ops=SimpleNamespace(import_scene=SimpleNamespace(gltf=import_gltf_stub)),
        data=SimpleNamespace(objects=[], materials={}),
    )

    monkeypatch.setattr(adapter, "bpy", bpy_stub)
    adapter.import_gltf(str(gltf_path))
    assert len(bpy_stub.data.objects) == expected_meshes
