---
title: "Acceptance Report Sprint L3-1"
version: 1.0.1
owner: "Robert Alexander Massinger"
license: "(c) COPYRIGHT 2023 - 2025 by Robert Alexander Massinger, Munich, Germany. ALL RIGHTS RESERVED."
history:
  - version: 1.0.1
    date: 2025-08-02
    change: "Translation to English"
    reference: "abnahmebericht-sprint-1.md"
---

# Acceptance Report Sprint L3-1

Acceptance of Sprint 1 from Sprint Plan L3:
(project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/sprint-plan-l3-step-gltf-integration-and-cad-detailing.md)

Certainly—I reviewed the current state of Sprint 1 based on the submitted changes, using the originally agreed plan as the yardstick.

### Achieved Results

* **Layer Model and Documentation**: A clear KERNEL → ADAPTER → GUI model has been described and documented, including an initial architecture overview and a library comparison for STEP and glTF. The foundation is laid.
* **Data Model**: With `data_model.py`, dataclasses for decks, hull, and an overall model now exist. This provides the necessary basis for data exchange.
* **Prototype Exporter**: Both a STEP exporter and a glTF exporter are available as prototypes. Tests ensure these functions produce runnable files.
* **Tests and Initial Integration Points**: A simple test module checks the generation of files; the construction handbook contains notes on the layer model and the transition to the new formats.

### Missing Points / Deltas

1. **Extensive Geometry Data in DTO**: Currently the deck objects contain only minimal data (inner radius, outer radius, height). Further values present in the core such as net radii, cylinder lengths, base and volume areas, and especially window and wormhole geometries are missing. These are necessary to fully populate the later STEP/glTF files.
   **What still needs to be done:** Extend the dataclasses to include all relevant fields from `SphereDeckCalculator` and introduce nested structures if necessary (e.g., lists of windows).

2. **Exporter Provides Only Metadata**: The current STEP and glTF exporters only generate comments or `extras` fields, but no actual geometry. For the prototype that's sufficient, but for Sprint 2 they must generate complete geometry as B-rep (STEP) or meshes with materials (glTF).
   **What still needs to be done:**

   * Use a library such as CadQuery for the STEP exporter to generate cylinders and spheres from radii and heights.
   * Use `trimesh` in the glTF exporter to create meshes representing decks, hull, wormhole, and base rings, and pack them into a glTF container.

3. **Integration into Existing Starters**: So far the new exporters are not called anywhere from the simulations. There are no CLI options or function calls to populate the `StationModel` from `SphereDeckCalculator` and then use the exporters.
   **What still needs to be done:** Extend the starter scripts (deck, hull, and station simulations) with parameters like `--export-step` / `--export-gltf` to populate the data model and call the respective exporter.

4. **Extend Test Coverage**: There is only a minimal test for file existence. In future the tests should check whether the number of exported decks matches the simulation and whether all relevant geometries are present in the STEP/glTF output.
   **What still needs to be done:** Write extended unit tests that parse the export (e.g., using a glTF parser or STEP reader) and validate the integrity of the data.

5. **Documentation Navigation**: Several files exist in the architecture folder, but the main README does not yet reference them.
   **What still needs to be done:** Add a table of contents to the main README and clearly link where each document is located.

### Recommendation

Sprint 1 is largely fulfilled, especially with regard to analysis and preparation. The next steps are to complete the data model, expand the exporters to be functional, and integrate them into the existing workflow. Please plan these items concretely for Sprint 2.

### Progress Since Acceptance

- The data model now includes a wormhole object with derived parameters in addition to decks and hull.
- The main README in the documentation folder now references the architecture documents and facilitates navigation.

