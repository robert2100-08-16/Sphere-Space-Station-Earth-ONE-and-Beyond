from pathlib import Path

from pygltflib import GLTF2

from simulations.sphere_space_station_simulations.simulation import StationSimulation
from simulations.sphere_space_station_simulations.adapters import (
    export_gltf,
    export_step,
)


def test_exported_files_can_be_imported(tmp_path: Path) -> None:
    sim = StationSimulation()
    model = sim.to_station_model()

    step_path = export_step(model, tmp_path / "station.step")
    gltf_path = export_gltf(model, tmp_path / "station.glb")

    assert step_path.exists() and step_path.stat().st_size > 0
    assert gltf_path.exists() and gltf_path.stat().st_size > 0

    # Verify that a viewer can load the glTF file
    gltf = GLTF2().load(str(gltf_path))
    assert gltf.meshes

    # Verify STEP placeholder header
    with step_path.open("r", encoding="utf-8") as handle:
        first_line = handle.readline().strip()
    assert first_line.startswith("STEP")
