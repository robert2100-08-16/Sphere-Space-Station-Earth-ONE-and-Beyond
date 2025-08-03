"""Tests for the Blender hull adapter.

The adapter relies on Blender's :mod:`bpy` module which is unavailable in the
test environment.  These tests patch in a minimal stub to ensure the script
invokes the expected Blender API calls and assigns materials to imported
objects.
"""

from types import SimpleNamespace

from simulations.blender_hull_simulation import adapter


def test_import_and_material_assignment(monkeypatch, tmp_path) -> None:
    called = {}

    def gltf(filepath: str) -> None:  # record the call for assertions
        called["path"] = filepath

    ops = SimpleNamespace(import_scene=SimpleNamespace(gltf=gltf))

    class Materials(dict):
        def get(self, name):
            return super().get(name)

        def new(self, name):
            mat = SimpleNamespace(name=name, diffuse_color=None)
            self[name] = mat
            return mat

    objects = [SimpleNamespace(type="MESH", data=SimpleNamespace(materials=[]))]

    bpy_stub = SimpleNamespace(
        ops=ops, data=SimpleNamespace(objects=objects, materials=Materials())
    )

    monkeypatch.setattr(adapter, "bpy", bpy_stub)

    fake_file = tmp_path / "station.glb"
    fake_file.touch()

    adapter.import_gltf(str(fake_file))
    adapter.assign_basic_material()

    assert called["path"] == str(fake_file)
    assert objects[0].data.materials[0].name == "HullMaterial"
