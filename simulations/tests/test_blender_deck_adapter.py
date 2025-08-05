"""Tests for the Blender deck adapter using a glTF import stub."""

from types import SimpleNamespace

from pygltflib import GLTF2

from simulations.blender_deck_simulator import adapter
from simulations.sphere_space_station_simulations.adapters.gltf_exporter import (
    export_gltf,
)
from simulations.sphere_space_station_simulations.data_model import Deck, StationModel


def test_import_and_material_assignment(monkeypatch, tmp_path) -> None:
    model = StationModel(decks=[Deck(1, 0.0, 1.0, 0.2)])
    gltf_path = export_gltf(model, tmp_path / "station.glb")
    gltf = GLTF2().load(str(gltf_path))
    expected_meshes = len(gltf.meshes)

    def import_gltf_stub(filepath: str) -> None:
        gltf_local = GLTF2().load(filepath)
        bpy_stub.data.objects = [
            SimpleNamespace(type="MESH", data=SimpleNamespace(materials=[]))
            for _ in gltf_local.meshes
        ]

    class Materials(dict):
        def get(self, name):
            return super().get(name)

        def new(self, name):
            mat = SimpleNamespace(name=name, diffuse_color=None)
            self[name] = mat
            return mat

    bpy_stub = SimpleNamespace(
        ops=SimpleNamespace(import_scene=SimpleNamespace(gltf=import_gltf_stub)),
        data=SimpleNamespace(objects=[], materials=Materials()),
    )

    monkeypatch.setattr(adapter, "bpy", bpy_stub)

    adapter.import_gltf(str(gltf_path))
    adapter.assign_basic_material()

    assert len(bpy_stub.data.objects) == expected_meshes
    assert bpy_stub.data.objects[0].data.materials[0].name == "DeckMaterial"
