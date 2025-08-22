---
title: "Sprint Plan L3: STEP/glTF Integration & CAD Detailing"
version: 1.0.1
owner: "Robert Alexander Massinger"
license: "(c) COPYRIGHT 2023 - 2025 by Robert Alexander Massinger, Munich, Germany. ALL RIGHTS RESERVED."
history:
  - version: 1.0.1
    date: 2025-08-02
    change: "Translation to English"
    reference: "sprintplan-l3-step-gltf-integration-und-cad-detailierung.md"
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

# 1. Sprint Plan for Simulations

## 1.1 Sprint Plan L3: STEP/glTF Integration & CAD Detailing

This sprint plan describes how the two major topics
(1) switching the simulations and animations to STEP and glTF and
(2) refining the CAD models over the coming months
will be implemented. It builds on the existing simulations and library structure of
`sphere_space_station_simulations` and develops them into a future-proof, layer-based
architecture (KERNEL → ADAPTER → GUI). The proposed sprints follow
two-week iterations with clear tasks, deadlines and deliverables.

### 1.1.1 Overall Goals

* **Unify CAD exchange format:**  
  All geometry (decks, hull, windows, etc.) is generated using a single precise CAD format. Due to its vendor independence and precision, STEP (ISO 10303) is chosen as the core format. Mathematical geometries (solids) can be exchanged accurately and losslessly.
* **Unify animation and visualization format:**  
  For animated scenes and interactive presentations glTF (alternatively USD) is introduced as the primary animation format. It is open, web-based, efficient and can be generated from Python.
* **Clean layering:**  
  The computation logic remains in the KERNEL (currently `geometry/`, `reporting/`, `animation/`); new ADAPTERS produce STEP, glTF, JSON or other DTOs; GUI layers (e.g., Blender scripts, web viewer, MATLAB plots) read exclusively from these adapter interfaces.
* **Detailed CAD models:**  
  Decks, hull, windows, corridors, docking ports, supply lines, etc. are geometrically refined. This results in mature models suitable for manufacturing, simulation and public relations.
* **Declassify CSV:**  
  The previously used CSV files for geometry transport (e.g., `deck_3d_construction_data.csv` in the Blender adapter) are replaced. CSV remains optional for reports, while structured data is transported via JSON/DTO and STEP/glTF.

The sprints start after completion of the existing library setup (sprint plan “sphere-space-station-simulations”, final date 26 Sep 2025). The new work begins on 29 Sep 2025.

---

## 1.2 Sprint 1 (29 Sep 2025 – 10 Oct 2025): Architecture Design & Technology Selection

### 1.2.1 Goals

1. Design a robust architecture for STEP/glTF integration.
2. Evaluate and select libraries for STEP and glTF generation.
3. Create first prototypes that output STEP and glTF files from existing geometry data.

### 1.2.2 Tasks

| Task | Target folder/module | Deadline |
| --- | --- | --- |
| Library research: evaluate Python libraries for STEP generation (e.g., pythonocc-core, CadQuery) and glTF (e.g., pygltflib, trimesh). Criteria: license, API stability, feature set, integration with Numpy/Pandas. | `docs/architecture/` | 01 Oct 2025 |
| Define layer model: create a document that clearly describes the KERNEL, ADAPTER and GUI layers. KERNEL includes classes like `SphereDeckCalculator`; ADAPTER contains exporters (STEP, glTF, JSON, HTML, CSV) and importers; GUI covers Blender scripts, web viewer, MATLAB scripts. | `docs/architecture/` | 03 Oct 2025 |
| Define data model/DTO: develop a unified data model (e.g., Python dataclasses) for exchange between KERNEL and adapters representing deck and hull geometry, materials and motion data. | `simulations/sphere_space_station_simulations/data_model.py` | 06 Oct 2025 |
| Prototype STEP exporter: implement an experimental exporter that writes the geometries computed in the KERNEL (deck cylinders and hull) into a STEP container using the evaluated library (e.g., pythonocc-core). | `simulations/sphere_space_station_simulations/adapters/step_exporter.py` | 10 Oct 2025 |
| Prototype glTF exporter: analogous to the STEP exporter, develop an initial glTF output (meshes) that transforms deck and hull data into a glTF file using, for example, pygltflib or trimesh. | `simulations/sphere_space_station_simulations/adapters/gltf_exporter.py` | 10 Oct 2025 |
| Unit tests: create simple tests for data model and prototype exporters (file is written, files can be opened). | `tests/test_adapters.py` | 10 Oct 2025 |

### 1.2.3 Deliverables

* Documented architecture with layer diagram.
* Evaluation report on STEP/glTF libraries.
* Basic data model (DTOs).
* First working exporters for STEP and glTF (without complete geometry yet).
* Test coverage for exporters.

---

## 1.3 Sprint 2 (13 Oct 2025 – 24 Oct 2025): Expand Adapters & Replace CSV

### 1.3.1 Goals

1. Develop complete STEP and glTF exporters that support all geometry from the KERNEL (deck cylinders, hull including wormhole and base rings, window geometry, rotation information).
2. Replace CSV as transport format and use it only for reports.
3. Convert existing Blender adapters to glTF import.

### 1.3.2 Tasks

| Task | Target folder/module | Deadline |
| --- | --- | --- |
| Finalize STEP exporter: extend the prototype so that the entire geometry model including window positions is written to STEP. Add material placeholders (e.g., steel, glass) as basis for later rendering info. | `adapters/step_exporter.py` | 16 Oct 2025 |
| Finalize glTF exporter: implement full mesh generation and scene description—decks as separate meshes, hull, wormhole and base rings; window holes as cut-outs; optional animations (rotation of the station) as glTF animation. | `adapters/gltf_exporter.py` | 16 Oct 2025 |
| JSON/DTO export: develop a JSON exporter that serializes the data model. This format serves data exchange (e.g., web apps) and is used by the STEP/glTF exporters. | `adapters/json_exporter.py` | 16 Oct 2025 |
| Revise Blender adapter: remove the CSV reader in existing Blender scripts (`blender_hull_simulation/adapter.py` etc.) and import the glTF file instead. In Blender the glTF is loaded via Python API and materials are assigned. | `simulations/blender_hull_simulation/adapter.py` | 20 Oct 2025 |
| Isolate CSV reporting: modify reporting functions (`reporting/deck.py`) so that CSV is only used for tabular evaluations (as before with `to_csv`). The geometry CSV (`deck_3d_construction_data.csv`) is removed. | `reporting/` | 20 Oct 2025 |
| Adjust CLI starters: starter scripts (deck, hull and station simulation) receive additional CLI options: `--export-step`, `--export-gltf` and `--export-json`, which generate the respective files. The CSV option remains for reports. | `simulations/deck_calculator/starter.py`, `simulations/blender_hull_simulation/starter.py` | 22 Oct 2025 |
| Extend tests: verify that STEP and glTF files contain all geometry (e.g., number of deck meshes equals number of decks, hull present). Ensure Blender import loads glTF correctly. | `tests/test_exporters.py` | 24 Oct 2025 |

### 1.3.3 Deliverables

* Extended geometry classes with additional parameters.
* STEP and glTF exporters with material and detail support.
* Animated glTF examples.
* Documented Blender scene and guide.
* Tests for detailed geometry.

---

## 1.4 Sprint 3 (27 Oct 2025 – 07 Nov 2025): Detail Geometry & Materials

### 1.4.1 Goals

1. Expand the geometry model with supports, corridors, window frames, emergency exits and docking ports.
2. Add material and color attributes.
3. Implement detail animations and Blender visualization.

### 1.4.2 Tasks

| Task | Target folder/module | Deadline |
| --- | --- | --- |
| Expand geometry model: extend `SphereDeckCalculator` with parameters for supports, corridors, window frames, emergency exits and docking ports. Implement calculations to determine positions and dimensions. | `geometry/deck.py`, `geometry/hull.py` | 31 Oct 2025 |
| Material and color properties: extend data model and exporters with material and color information (e.g., steel, aluminum, glass; color as RGB). These details are stored as PBR materials in glTF and as metadata in STEP. | `data_model.py`, `adapters/gltf_exporter.py`, `adapters/step_exporter.py` | 31 Oct 2025 |
| Detail animations: implement additional animations for glTF, e.g., opening/closing docking ports, rotating individual decks for maintenance. | `adapters/gltf_exporter.py` | 03 Nov 2025 |
| Prototype visualization in Blender: create an example scene that imports the detailed model with materials and renders it. Document how to load and further process the glTF file in Blender. | `recommendations/blender_example_scene.blend` (or markdown doc) | 07 Nov 2025 |
| Tests for details: add unit tests that check, for example, that the number of docking ports in STEP matches the simulation and that glTF contains corresponding mesh groups. | `tests/test_geometry_details.py` | 07 Nov 2025 |

### 1.4.3 Deliverables

* Extended geometry classes with additional parameters.
* STEP and glTF exporters with material and detail support.
* Animated glTF examples.
* Documented Blender scene and guide.
* Tests for detailed geometry.

---

## 1.5 Sprint 4 (10 Nov 2025 – 21 Nov 2025): Integration, Documentation & Quality Assurance

### 1.5.1 Goals

1. Integrate and stabilize all new components.
2. Create comprehensive documentation in German and English.
3. Set up automated quality checks and CI.

### 1.5.2 Tasks

| Task | Target folder/module | Deadline |
| --- | --- | --- |
| Integration tests: write end-to-end tests covering the full flow: compute geometry → export to STEP/glTF → import into Blender/web viewer → render/visualize. | `tests/test_integration.py` | 14 Nov 2025 |
| Update documentation: expand README and API docs bilingually (DE/EN); provide migration notes for the STEP/glTF transition; examples for new CLI options; explain the layer model. | `README.md`, `docs/` | 18 Nov 2025 |
| Refactoring & cleanup: remove outdated CSV adapters and scripts; unify naming conventions; perform PEP8 cleanups. | entire repository | 18 Nov 2025 |
| Continuous Integration (CI): define a CI workflow (GitHub Actions) that runs tests for Python, STEP/glTF exports and Blender scripts. Optionally upload artifacts (glTF/STEP examples). | `.github/workflows/ci.yml` | 21 Nov 2025 |
| Stakeholder review & feedback: present results (STEP file, glTF scene, rendering). Collect feedback (e.g., on detail accuracy, file sizes) and create backlog for further iterations. | `project/backlog.md` | 21 Nov 2025 |

### 1.5.3 Deliverables

* Complete STEP/glTF export pipeline including automated tests.
* Bilingual documentation and migration guide.
* CI workflow for quality control.
* Clean repository without obsolete CSV scripts.
* Feedback log for future improvements.

---

## 1.6 Notes & Rationale for Tool Choice

* **STEP as CAD format:**  
  The main advantage of STEP is its precision and vendor-independent description of complex solids. While OBJ or STL are easier to generate, they lose B-rep information; therefore STEP is used for the core geometry.
* **glTF for animations:**  
  glTF is compact, web-based and natively supported by Blender. It allows material and animation definitions and can be generated with Python libraries.
* **USD as option:**  
  USD remains an option for very large scenes and may be evaluated in a later sprint.
* **Clear layer model:**  
  The existing library structure with `geometry/`, `reporting/` and `animation/` forms the core (KERNEL). New ADAPTERS translate the computed geometry into STEP/glTF/JSON/CSV and dissolve the previous direct coupling (e.g., CSV readers in Blender scripts). GUI layers like the Blender scripts should in future only access these adapters and contain no own computation logic.
* **CSV still for reports:**  
  Functions like `to_csv()` remain as reporting tools but are no longer used for geometry transport. Switching to structured DTOs and STEP/glTF reduces duplicate implementations and increases consistency.

---

## 1.7 Footnotes

1. https://chatgpt.com/?utm_src=deep-research-pdf
2. https://chatgpt.com/?utm_src=deep-research-pdf
3. https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/README.md#L3-L11
4. https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/recommendations/blender_simulation_recommendations.md#L10-L24
5. https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/blender_hull_simulation/adapter.py#L1-L37
6. https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/geometry/hull.py#L6-L67
7. https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/geometry/deck.py#L97-L133
8. https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/reporting/deck.py#L46-L58
9. https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/recommendations/blender_simulation_recommendations.md
10. https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/README.md
11. https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/recommendations/blender_simulation_recommendations.md#L10-L24

