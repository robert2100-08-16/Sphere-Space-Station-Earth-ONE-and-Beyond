import sys
import os
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Use the standard library only for CSV handling
import csv

from simulations.sphere_space_station_simulations.data_preparation import (
    generate_deck_construction_csv,
)


def test_generate_deck_construction_csv(tmp_path):
    input_csv = tmp_path / "deck_dimensions.csv"
    header = (
        ",deck_id,inner_radius_m,outer_radius_m,outer_radius_netto_m,ceiling_thickness_m,"
        "deck_height_m,deck_inner_height_m,length_inner_radius_m,length_outer_radius_m,"
        "length_outer_radius_netto_m,base_area_inner_radius_m2,base_area_outer_radius_m2,"
        "effective_volume_m3,net_room_volume_m3,rotation_velocity_mps,centrifugal_acceleration_mps2"
    )
    rows = [
        "0,Deck_000,1.0,1.5,1.4,0.5,0.0,3.0,0,0,0,0,0,0,0,0.1,0.0",
        "1,Deck_001,2.0,2.5,2.4,0.5,0.0,3.0,0,0,0,0,0,0,0,0.2,0.1",
    ]
    csv_text = "Deck Dimensions of a Sphere\n" + header + "\n" + "\n".join(rows) + "\n"
    input_csv.write_text(csv_text, encoding="ISO-8859-1")

    output_csv = tmp_path / "out.csv"
    path = generate_deck_construction_csv(input_csv, output_csv)
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows_out = list(reader)
    assert len(rows_out) == 2
    assert "deck_usage" in rows_out[0]


def test_starter_builds_command(monkeypatch, tmp_path):
    calls = []

    def fake_run(cmd, check):
        calls.append(cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setenv("BLENDER_PATH", "blender")
    script = tmp_path / "adapter.py"
    script.write_text("")

    argv = ["starter.py", "--script", str(script), "--background"]
    monkeypatch.setattr("sys.argv", argv)

    from simulations.blender_deck_simulator.starter import main

    main()
    assert calls
    assert calls[0][0] == "blender"
    assert "--python" in calls[0]
