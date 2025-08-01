import sys
import os
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pandas as pd

from simulations.sphere_space_station_simulations.data_preparation import (
    generate_deck_construction_csv,
)


def test_generate_deck_construction_csv(tmp_path):
    input_csv = tmp_path / "deck_dimensions.csv"
    df = pd.DataFrame(
        {
            "deck_id": ["Deck_000", "Deck_001"],
            "inner_radius_m": [1.0, 2.0],
            "outer_radius_m": [1.5, 2.5],
            "outer_radius_netto_m": [1.4, 2.4],
            "deck_inner_height_m": [3.0, 3.0],
            "rotation_velocity_mps": [0.1, 0.2],
            "centrifugal_acceleration_mps2": [0.0, 0.1],
        }
    )
    csv_text = "header\n" + df.to_csv(index=False)
    input_csv.write_text(csv_text, encoding="ISO-8859-1")

    output_csv = tmp_path / "out.csv"
    path = generate_deck_construction_csv(input_csv, output_csv)
    out_df = pd.read_csv(path)
    assert len(out_df) == 2
    assert "deck_usage" in out_df.columns


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
