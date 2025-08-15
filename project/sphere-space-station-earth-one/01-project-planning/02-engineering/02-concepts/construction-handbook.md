---
title: "Construction Handbook"
version: 1.1.3
owner: "Robert Alexander Massinger"
license: "(c) COPYRIGHT 2023 - 2025 by Robert Alexander Massinger, Munich, Germany. ALL RIGHTS RESERVED."
history:
  - version: 1.1.3
    date: 2025-08-18
    change: "EV0 deck now exports glTF with materials; CadQuery usage under review"
  - version: 1.1.2
    date: 2025-08-15
    change: "Documented DECK000 EV0 geometry export"
  - version: 1.1.1
    date: 2025-08-10
    change: "Corrected window material handling in STEP exporter"
  - version: 1.1.0
    date: 2025-08-08
    change: "Integrated deck supports and docking port planning into simulation"
  - version: 1.0.0
    date: 2024-10-30
    change: "Initial"
    reference: Project_SpaceBall_20230318.pdf
---
# 1. Construction Handbook

This handbook collects key decisions for modeling the Sphere Space Station and serves as ongoing documentation.

## 1.1 Current Status

- **Deck data** are based on calculations from `deck_calculations_script.py`; Blender consumes the glTF export `station.glb` instead of an intermediate CSV.
- **Variable names** were converted to a consistent, PEP8-compliant schema (e.g., `deck_id`, `inner_radius_m`).
- **Blender scripts** import the glTF model and assign materials. Optional energy and thermal systems such as radiators, SMRs, and solar arrays are added for realism.
- **Realistic simulation**: Materials, windows and basic energy systems are configured automatically when importing the model.
- **Acceleration visualization**: When generating decks, the color is now derived from centrifugal acceleration (0 m/s² → white, 9.81 m/s² → green, higher values shift toward red).
- **Convenient launch**: `starter.py` launches Blender using the `BLENDER_PATH` environment variable. A VS Code launch configuration simplifies execution.
- **Hull simulation**: An additional script `adapter.py` creates a simplified outer hull. A dedicated VS Code launch entry makes it easy to test the script.
- **Blender helpers** reside in the subpackage `blender_helpers` and are imported by the adapter.
- **Hull geometry** is computed by `geometry/hull.py` and imported by the deck logic.
- **Deck evolution modules**: EV0 adds baseline DECK000 tube segments with OBJ+CSV export.
- **EV0 enhancements**: Material support added to segments and glTF export complements OBJ+CSV outputs. CadQuery remains optional pending dependency trade-offs.
- **Deck supports and docking ports** can be parametrized in `SphereDeckCalculator`,
  enriching the structural model with columns and equatorial docking locations.
- **Station simulation** has moved to `simulation.py` and can be started directly from the library. `run_simulation.py` is now called `starter.py`.
- **glTF-based hull import**: `blender_hull_simulation/adapter.py` loads the geometry from a glTF file exported by `gltf_exporter.py` and assigns a simple material, removing the previous CSV dependency.
- **CSV transport removed**: `deck_3d_construction_data.csv` and its generator were dropped; CSV is retained only for reports such as `results/deck_dimensions.csv`.
- **Layered model**: KERNEL, ADAPTER, and GUI were defined as distinct layers.
- **Data model**: Dataclasses for decks and hull enable export.
- **Prototype exporter**: Initial STEP and glTF files are generated from the data objects.
- **CLI exporter**: Starter scripts now support `--export-step`, `--export-gltf`, and `--export-json` to output geometry files; CSV remains as reporting output.
- **Detailed data model**: `Deck` and `Hull` include net radii, cylinder lengths, base areas, and volumes, and support nested window specifications (position, size, count).
- **CAD and glTF exporters**: STEP files now contain B-rep solids with material placeholders (steel/glass); the glTF export generates meshes with PBR materials and a simple rotation animation.
- **Window materials**: STEP exporter uses material settings from `Window` instances instead of CadQuery solids.
- **STEP archiving**: The generated `station.step` is stored as the Base64 file `station.step.base64` to avoid binary diffs.

Further adjustments and releases will be added to this document.

## 1.2 Sources

No external sources used.
