---
title: "Software Design Decisions"
version: 1.2.0
owner: "Robert Alexander Massinger"
license: "(c) COPYRIGHT 2023 - 2025 by Robert Alexander Massinger, Munich, Germany. ALL RIGHTS RESERVED."
history:
  - version: 1.2.0
    date: 2025-08-05
    change: "Automatic glTF generation for Blender via prepare_scene"
  - version: 1.1.0
    date: 2025-02-14
    change: "Added BaseRing DTO, material metadata and exporter tests"
  - version: 1.0.0
    date: 2024-10-30
    change: "Initial"
    reference: Project_SpaceBall_20230318.pdf
---
# 1. Software Design Decisions

This document summarizes important architectural decisions of the Python software. The goal is a long-term maintainable library
for calculations and 3D simulations of the Sphere Space Station.

## 1.1 Evaluation of Approaches

**Approach 1 – Modular Python Library**
- Functions are encapsulated in clearly separated modules and can be used by various adapters (e.g., Blender, MATLAB).
- Shared tests and a uniform API facilitate maintenance and reuse.

**Approach 2 – Continuing the Script**
- Rapid extensions are possible, but the script would grow into a hard-to-maintain monolith over time.
- Additional adapters would have to be developed individually each time.

## 1.2 Decision

To make the simulation versatile and easier to test, Approach 1 is being implemented. A standalone Python library is being created under `simulations/library`. The existing script will remain for now; a new `deck_calculations_adapter.py` serves as a bridge between the library and current workflows.

## 1.3 Sources

No external sources used.

## 1.4 STEP/glTF/JSON Export

- Station geometry is computed via `SphereDeckCalculator` and transformed into a structured `StationModel`.
- Exporters write STEP, glTF and JSON files which serve as the primary interchange formats.
- Blender adapters import the generated glTF directly; the helper CSV `deck_3d_construction_data.csv` was removed and CSV remains only for analytical reports such as `results/deck_dimensions.csv`.
- The data model now includes `BaseRing` elements and material/colour properties for all geometry. Exporters and tests ensure that rings and materials are preserved across STEP, glTF and JSON workflows.
- A helper `prepare_scene` script automatically creates the required `station.glb`
  file when Blender adapters run, reducing manual export steps.
