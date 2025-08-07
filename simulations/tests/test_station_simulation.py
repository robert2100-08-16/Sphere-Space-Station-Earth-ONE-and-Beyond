import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from simulations.sphere_space_station_simulations.simulation import StationSimulation


def test_models_load():
    sim = StationSimulation(
        enable_docking=False,
        enable_mission_control=False,
        enable_life_support=False,
        enable_emergency_drills=False,
    )
    assert sim.decks is not None
    assert sim.hull is not None


def test_cli_export_options(tmp_path, monkeypatch):
    from simulations.sphere_space_station_simulations import simulation

    called = {}

    def fake_step(model, path):
        called["step"] = path
        return path

    def fake_gltf(model, path):
        called["gltf"] = path
        return path

    def fake_json(model, path):
        called["json"] = path
        path.write_text("{}", encoding="utf-8")
        return path

    monkeypatch.setattr(simulation, "export_step", fake_step)
    monkeypatch.setattr(simulation, "export_gltf", fake_gltf)
    monkeypatch.setattr(simulation, "export_json", fake_json)

    step = tmp_path / "station.step"
    gltf = tmp_path / "station.glb"
    json_path = tmp_path / "station.json"

    simulation.main(
        [
            "--export-step",
            str(step),
            "--export-gltf",
            str(gltf),
            "--export-json",
            str(json_path),
            "--no-docking",
            "--no-mission-control",
            "--no-life-support",
            "--no-emergency",
        ]
    )

    assert called["step"] == step
    assert called["gltf"] == gltf
    assert called["json"] == json_path


def test_cli_material_options(tmp_path, monkeypatch):
    from simulations.sphere_space_station_simulations import simulation

    captured = {}

    def fake_json(model, path):
        captured["deck"] = model.decks[0].material.name
        captured["hull"] = model.hull.material.name if model.hull else None
        path.write_text("{}", encoding="utf-8")
        return path

    monkeypatch.setattr(simulation, "export_json", fake_json)

    json_path = tmp_path / "station.json"

    simulation.main(
        [
            "--export-json",
            str(json_path),
            "--deck-material",
            "Aluminium",
            "--hull-material",
            "Polymer",
            "--no-docking",
            "--no-mission-control",
            "--no-life-support",
            "--no-emergency",
        ]
    )

    assert captured["deck"] == "Aluminium"
    assert captured["hull"] == "Polymer"
