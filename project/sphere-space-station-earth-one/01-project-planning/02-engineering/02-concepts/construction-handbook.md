---
title: "Construction Handbook"
version: 1.0.0
owner: "Robert Alexander Massinger"
license: "(c) COPYRIGHT 2023 - 2025 by Robert Alexander Massinger, Munich, Germany. ALL RIGHTS RESERVED."
history:
  - version: 1.0.0
    date: 2024-10-30
    change: "Initial"
    reference: Project_SpaceBall_20230318.pdf
---
# 1. Construction Handbook

This handbook collects key decisions for modeling the Sphere Space Station and serves as ongoing documentation.

## 1.1 Current Status

- **Deck data** are based on calculations from `deck_calculations_script.py` and are prepared for Blender in `deck_3d_construction_data.csv`.
- **Variable names** were converted to a consistent, PEP8-compliant schema (e.g., `deck_id`, `inner_radius_m`).
- **Blender scripts** generate realistically proportioned decks and a central wormhole. Materials and windows are set using the CSV data.
- **Realistic simulation**: The Blender script now assigns materials, places windows automatically, and adds energy and thermal systems such as radiators, SMRs, and solar arrays. Light sources are oriented to deck functions.
- **Acceleration visualization**: When generating decks, the color is now derived from centrifugal acceleration (0 m/s² → white, 9.81 m/s² → green, higher values shift toward red).
- **Convenient launch**: `starter.py` launches Blender using the `BLENDER_PATH` environment variable. A VS Code launch configuration simplifies execution.
- **Hull simulation**: An additional script `adapter.py` creates a simplified outer hull. A dedicated VS Code launch entry makes it easy to test the script.
- **CSV generator** `generate_deck_construction_csv` is now part of the `data_preparation.py` library and is used by `generate_3d_construction_csv.py`.
- **Blender helpers** reside in the new subpackage `blender_helpers` and are imported by the adapter.
- **Hull geometry** is now computed by `geometry/hull.py` and imported by the deck logic.
- **Station simulation** has moved to `simulation.py` and can be started directly from the library. `run_simulation.py` is now called `starter.py`.

- **Import path**: `adapter.py` adds the repository root to `sys.path`, allowing Blender to locate the helper functions properly.

- **Reduced dependencies**: `generate_deck_construction_csv` no longer requires Pandas and the package uses lazy imports so the Blender adapters run without extra libraries.
- **Hull starter**: The hull simulation's `starter.py` now points to `adapter.py` by default.
- **glTF-based hull import**: `blender_hull_simulation/adapter.py` loads the
  geometry from a glTF file exported by `gltf_exporter.py` and assigns a simple
  material, removing the previous CSV dependency.

- **Deck rendering**: `create_ring_deck` now only removes the inner helper geometry so all decks, not just the wormhole, appear. The deck ID is now parsed correctly based on the underscore so windows are created for the first twelve decks.

- **Layered model**: KERNEL, ADAPTER, and GUI were defined as distinct layers.
- **Data model**: Dataclasses for decks and hull enable export.
- **Prototype exporter**: Initial STEP and glTF files are generated from the data objects.

- **CLI exporter**: Starter scripts now support `--export-step`, `--export-gltf`, and `--export-json` to output geometry files; CSV remains as reporting output.

- **Detailed data model**: `Deck` and `Hull` include net radii, cylinder lengths, base areas, and volumes, and support nested window specifications (position, size, count).

- **CAD and glTF exporters**: STEP files now contain B-rep solids with material placeholders (steel/glass); the glTF export generates meshes with PBR materials and a simple rotation animation.

- **STEP archiving**: The generated `station.step` is stored as the Base64 file `station.step.base64` to avoid binary diffs.

Further adjustments and releases will be added to this document.

## 1.2 Sources

No external sources used.
