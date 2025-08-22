---
title: "Second Acceptance Report Sprint L3-2"
version: 1.0.1
owner: "Robert Alexander Massinger"
license: "(c) COPYRIGHT 2023 - 2025 by Robert Alexander Massinger, Munich, Germany. ALL RIGHTS RESERVED."
history:
  - version: 1.0.1
    date: 2025-08-05
    change: "Translation to English"
    reference: "2-abnahmebericht-sprint-2.md"
id: ""
state: DRAFT
evolution: ""
discipline: ""
system: []
system_id: []
seq: []
reviewers: []
source_of_truth: false
supersedes: null
superseded_by: null
rfc_links: []
adr_links: []
cr_links: []
lang: EN
---

# Second Acceptance Report Sprint L3-2

As Product Owner I conducted the second acceptance of Sprint 2 based on Sprint Plan L3 “STEP/glTF Integration & CAD Detailing” and reviewed the current state in the repository. The sprint plan for Sprint 2 (13–24 Oct 2025) foresees the following tasks and deliverables: final STEP and glTF exporters with all geometry, JSON/DTO export, revision of the Blender adapter, replacement of CSV geometry, extension of starter scripts with export options and expanded tests.

### Completed Points

* **STEP Exporter:** In `simulations/sphere_space_station_simulations/adapters/step_exporter.py` there is now a STEP exporter that creates deck and hull geometries as well as the wormhole as B-rep solids and assigns material metadata (“steel” or “glass”). When the CadQuery library is missing a small placeholder file is generated.
* **glTF Exporter:** The glTF exporter generates triangulated meshes for decks and the hull, cuts window openings and adds PBR materials. It also includes a simple rotation animation of the entire station.
* **JSON Exporter:** A lightweight JSON exporter serializes the entire data model via `dataclasses.asdict` into a readable JSON file.
* **Blender Adapter:** The former CSV-based adapter has been replaced by `simulations/blender_hull_simulation/adapter.py`; this now loads the glTF file directly and assigns a simple material to all mesh objects.
* **CLI Starters:** The starter scripts for deck and hull simulations now provide export options for STEP, glTF and JSON and optionally still generate a CSV report. The hull starter script also forwards additional arguments to Blender.
* **CSV Deprecated:** The file `deck_3d_construction_data.csv` no longer exists; CSV is only used as a report (e.g., `to_csv` in reporting).

### Additions Since the Last Acceptance

* **Base Rings:** The data model `StationModel` now includes `BaseRing` elements. STEP and glTF exporters generate dedicated geometry with material metadata for them.
* **Tests:** `simulations/tests/test_exporters.py` checks all export paths and verifies that Blender can import the generated glTF files including base rings.
* **JSON/DTO:** Materials and base rings are fully supported through an extended JSON exporter as well as a matching importer.
* **Documentation:** The README explains the new CLI options (`--export-step`, `--export-gltf`, `--export-json`) and describes the switch from CSV to STEP/glTF/JSON.

### Summary

The core tasks from Sprint 2 have now been fully implemented: functional STEP and glTF exporters with material metadata, JSON exporter and importer, extensive tests and updated documentation. Sprint 2 is therefore considered complete.

