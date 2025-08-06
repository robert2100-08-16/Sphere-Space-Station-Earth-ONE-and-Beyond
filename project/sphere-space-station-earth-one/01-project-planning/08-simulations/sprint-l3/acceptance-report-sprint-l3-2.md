---
title: "Acceptance Report Sprint L3-2"
version: 1.0.1
owner: "Robert Alexander Massinger"
license: "(c) COPYRIGHT 2023 - 2025 by Robert Alexander Massinger, Munich, Germany. ALL RIGHTS RESERVED."
history:
  - version: 1.0.1
    date: 2025-08-05
    change: "Translation to English"
    reference: "abnahmebericht-sprint-2.md"
---

# Acceptance Report Sprint L3-2

When reviewing Sprint 2 based on the current repository state (branch `main`), the following findings and deltas compared to the sprint plan emerge:

### Completed Points

* **STEP Exporter**: The exporter creates real B-rep solids for decks and hull with CadQuery; windows are generated as separate solids, and materials (steel/glass) are stored as metadata. In fallback mode without CadQuery a placeholder is generated.
* **glTF Exporter**: The exporter tessellates decks, hull and wormhole, cuts window holes, generates glass meshes and assigns PBR materials; a simple rotation animation is included.
* **JSON Exporter**: A simple exporter serializes the complete data model to JSON using `asdict`.
* **Data Model Expanded**: `data_model.py` now contains window definitions, net dimensions as well as automatically calculated base areas and volumes.
* **CLI Starters for Deck and Hull Simulation**: The starters accept `--export-step`, `--export-gltf` and `--export-json` and generate the corresponding files.
* **Blender Adapter (Hull)**: The new adapter loads glTF files directly into Blender and assigns basic materials; the CSV reader from Sprint 1 was removed here.
* **Tests Extended**: Tests verify that the glTF exporter creates the correct number of meshes and that JSON contains all new fields (not quoted in detail but present).

### Deltas and Missing Implementations

1. **Blender Deck Adapter still CSV-based**: The module `blender_deck_simulator/adapter.py` still reads a CSV file to generate decks, windows and solar arrays. According to the sprint plan, geometry should be imported via glTF.
   **Open:** Integrate the functions for creating decks, windows and auxiliary structures into the glTF exporter or the data model so that the Blender adapter only needs to load the glTF (similar to the hull adapter). Afterwards remove the CSV file and `generate_3d_construction_csv.py`.

2. **CSV Transport not Completely Replaced**: In addition to the Blender adapter, the 3D construction CSV (`deck_3d_construction_data.csv`) and the associated documentation in `blender_deck_simulator/description.md` still exist. The sprint plan stipulates using CSV only for reporting.
   **Open:** Delete the CSV-based deck model or move it to an example report. The information previously transported via CSV (number of windows, material choice, rotation speeds) belongs in the data model and the glTF exporter.

3. **Tests for STEP Export and Blender Import**: Existing tests mainly cover glTF export and JSON. A test that checks the STEP exporter with CadQuery (e.g., number of generated B-rep bodies) is missing, as is one that runs the new Blender adapter and ensures all objects are imported correctly.
   **Open:** Add further tests: (1) open the STEP file with a STEP parser and verify that decks, hull and wormhole are present; (2) run the Blender import with `bpy` (e.g., in CI with headless Blender) and ensure the object count matches the glTF.

4. **CLI Hook-Up for Station Simulation**: The high-level station simulation (combined deck and hull model) imports the `SphereDeckCalculator` but offers no options for STEP/glTF export.
   **Open:** Here too, add `--export-step`, `--export-gltf` and `--export-json` options that create the shared `StationModel` and pass it to the exporters.

5. **Documentation Update**: The architecture README lacks clear navigation to the STEP, glTF and JSON exporters. It should also explain that the Blender deck adapter will be dropped.
   **Open:** Add a README to the architecture folder that documents the switch to glTF, explains the remaining use of CSV for reports and describes the exporter interfaces.

### Conclusion

The core tasks of the sprint—functional STEP/glTF exporters and a JSON format—have been implemented successfully. The CLI integration and glTF-based hull import into Blender meet expectations as well. However, the complete removal of CSV transport paths has not yet been achieved: the Blender deck adapter still works with CSV and the related files still exist. Sprint 3 should focus on removing these legacy elements, mapping all geometry information through the data model and exporters, and expanding test coverage for STEP import and Blender integration.

### Update

The open points mentioned have now been addressed:
- The Blender deck adapter now loads glTF files and all CSV helper files have been removed.
- Additional tests check STEP export and glTF import in Blender.
- The station simulation offers export options for STEP, glTF and JSON.
- The architecture documentation references all exporters and explains the remaining use of CSV for reports.

