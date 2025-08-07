---
title: "Sprint Plan L4: Full‑Simulator & Module Integration" 
version: 1.0.0 
owner: "Robert Alexander Massinger" 
license: "(c) COPYRIGHT 2023 - 2025 by Robert Alexander Massinger, Munich, Germany. ALL RIGHTS RESERVED." 
history: 
  - version: 1.0.0 
    date: 2025-08-06 
    change: "Initial creation of the sprint plan for a full simulation with optional modules" 
reference: "sprint‑l4‑full‑simulation‑story.md"
---

# Sprint Plan L4: Full‑Simulator & Module Integration

## Overview

The fourth simulation sprint extends the scope of the project beyond decks and hull to build a full station simulator. Based on the task analysis in the story document for sprint L4 and the technical documentation, the sprint introduces optional sub‑systems—transport, energy, safety, docking, propulsion, life support and other facilities—into the scene model[^1]. It also integrates outstanding work from the backlog such as end‑to‑end tests, documentation updates, removal of CSV references and a continuous‑integration workflow[^2]. The sprint follows a two‑week iteration from 10 Nov 2025 – 21 Nov 2025, immediately after sprint L3[^3].

## Goals

1. **Modular scene architecture** – Define a SceneModel that encapsulates the base geometry (decks, hull, wormhole, base rings) and allows optional modules (transport systems, reactors, safety devices, docking/freight bays, thrusters, life support, hydroponics, labs, etc.) to be toggled via configuration[^4].

2. **Implement modules** – Create geometric placeholders or detailed models for the systems identified in the technical documents:
   - Heavy elevators, conveyor belts and hover channels
   - SMR and reserve reactors, solar panels, thermal storage and radiators
   - Fire‑safety doors, radiation shields, MMOD protection and evacuation capsules
   - Central docking port, freight/waste bays and shuttle placeholders
   - Gyroscopes, reaction wheels and thrusters
   - Recycling and hydroponics units, medical and industrial facilities[^1][^4]

3. **Configuration and control** – Design a TOML/JSON configuration (full_scene.toml) and extend prepare_full_scene.py so that each module can be enabled or disabled via configuration or CLI flags[^5].

4. **Quality assurance** – Develop end‑to‑end tests for STEP and glTF exports and validate module activation/deactivation in Blender and web viewers[^6][^7].

5. **Documentation & CI** – Update project documentation bilingually with CLI examples and layer model description, remove legacy CSV references, perform PEP 8 clean‑ups and establish a CI workflow that runs tests and validates exporters/blender scripts[^8][^9].

## Tasks

| Task | Target folder/module | Deadline |
|------|---------------------|----------|
| Architecture definition (L4‑T1): Design the SceneModel class and configuration schema. The model should include base elements (decks, hull, wormhole, base rings) and an extensible list of modules, each controlled via an include_<module> flag. Document the class in code and prepare sample config files. | `simulations/sphere_space_station_simulations/data_model.py`, `simulations/sphere_space_station_simulations/scene_model.py` | 12 Nov 2025 |
| Transport systems (L4‑T2): Implement geometric representations for heavy radial lifts, tangential conveyor belts/tracks and hover/climbing channels. Add DTOs for these systems and integrate them into the SceneModel. Provide optional mesh detail depending on module parameters. | `geometry/transport.py`, `data_model.py`, `adapters/step_exporter.py`, `adapters/gltf_exporter.py` | 13 Nov 2025 |
| Energy subsystems (L4‑T3): Create placeholder models for two NuScale SMR reactors, reserve reactors, large solar‑panel arrays, thermal storage tanks and radiators[^10]. Assign appropriate materials (e.g. steel, glass, black coatings) and incorporate them as modules in the scene model. | `geometry/energy.py`, `data_model.py`, `adapters/*` | 13 Nov 2025 |
| Safety modules (L4‑T4): Add fire‑safety doors/partitions, inert‑gas and water‑mist extinguishing systems, radiation shields, micrometeoroid protection layers and evacuation capsules to the model[^11]. Define DTOs and geometry generation functions for these components and link them to module flags. | `geometry/safety.py`, `data_model.py`, `adapters/*` | 14 Nov 2025 |
| Docking & freight (L4‑T5): Design and implement a central docking port on deck 000, freight and waste bays with processing facilities and shuttle placeholders[^12]. Provide geometry and materials for these features and integrate into the model. | `geometry/docking.py`, `data_model.py`, `adapters/*` | 15 Nov 2025 |
| Attitude & propulsion (L4‑T6): Model gyroscopes, reaction wheels and electric thrusters used for attitude control and orbit adjustments[^13]. Incorporate these as optional modules and assign material/animation placeholders. | `geometry/propulsion.py`, `data_model.py`, `adapters/*` | 15 Nov 2025 |
| Life support & infrastructure (L4‑T7): Implement closed air/water/waste recycling systems, hydroponics and bioreactors, plus optional placeholders for medical centres, recreation areas and industrial labs[^14]. Define DTOs and include them in the scene model. | `geometry/life_support.py`, `data_model.py`, `adapters/*` | 16 Nov 2025 |
| Configuration & CLI (L4‑T8): Develop full_scene.toml with boolean flags for each module and implement a parser in prepare_full_scene.py. Extend the CLI (e.g. starter.py) to accept parameters like --include-energy, --exclude-docking and pass them into the scene builder[^5]. | `simulations/prepare_full_scene.py`, `simulations/starter.py` | 17 Nov 2025 |
| Integration tests (L4‑T9): Write automated end‑to‑end tests that verify the following flow: build a scene with different module combinations → export to STEP and glTF → import into Blender/web viewer → check that the correct modules appear. These tests also cover reading/writing of full_scene.toml and CLI flags[^6][^7]. | `tests/test_full_scene.py`, `tests/test_integration.py` | 18 Nov 2025 |
| Documentation & examples (L4‑T10): Update README and create a new Full‑Simulator guide in both German and English. Provide example configuration files (minimal/full), CLI usage examples and a description of the layer model. Document new DTOs and modules. Remove outdated CSV references and ensure code follows PEP 8 naming conventions[^15][^16]. | `README.md`, `docs/full_simulator.md`, repository-wide | 20 Nov 2025 |
| Continuous integration (L4‑T11): Set up a GitHub Actions workflow that runs unit and integration tests, builds STEP/glTF outputs and optionally renders them in Blender (using command‑line rendering). Publish artifacts for visual inspection. Add a separate job to validate PEP 8 compliance and type hints[^17][^18]. | `.github/workflows/ci.yml` | 21 Nov 2025 |
| Stakeholder review & backlog update (L4‑T12): Present the full‑simulator outputs (STEP files, glTF scenes, Blender renders) to stakeholders. Collect feedback on accuracy, modularity and performance and update the backlog accordingly[^19]. | `project/backlog.md` | 21 Nov 2025 |

## Deliverables

- Modular SceneModel class and configuration schema enabling optional sub‑systems.
- Geometric implementations for transport, energy, safety, docking, propulsion, life support and facility modules with appropriate materials and placeholder animations.
- Configurable CLI and parser to assemble scenes via full_scene.toml or command‑line flags.
- End‑to‑end tests verifying module activation and export/import of STEP and glTF models.
- Comprehensive documentation in German and English, example configuration files and CLI tutorials.
- Continuous‑integration workflow running tests and validations, including Blender rendering.
- Stakeholder feedback report and updated backlog for future sprints.

## Integration with Previous Sprints and Backlog

This sprint builds upon the cad‑detailing work of sprint L3 and the integration/documentation tasks originally planned for sprint 4[^3]. By modelling the additional systems listed in the technical documentation and providing configuration, testing and CI, the team can deliver a fully interactive simulator while ensuring technical debt (CSV files, inconsistent naming) is addressed[^8]. Any remaining suggestions from stakeholders will be captured and prioritised in the backlog for subsequent sprints.

[^1]: [Technical Documentation - Sprint L4 Story](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l4/sprint-l4-full-simulation-story.md)
[^2]: [Backlog Documentation](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/backlog.md)
[^3]: [Sprint L3 Plan](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/sprint-plan-l3-step-gltf-integration-and-cad-detailing.md)
[^4]: [Technical Documentation - Sprint L4 Story](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l4/sprint-l4-full-simulation-story.md)
[^5]: [Technical Documentation - Sprint L4 Story](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l4/sprint-l4-full-simulation-story.md)
[^6]: [Technical Documentation - Sprint L4 Story](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l4/sprint-l4-full-simulation-story.md)
[^7]: [Backlog Documentation](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/backlog.md)
[^8]: [Backlog Documentation](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/backlog.md)
[^9]: [Sprint L3 Plan](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/sprint-plan-l3-step-gltf-integration-and-cad-detailing.md)
[^10]: [Technical Documentation - Sprint L4 Story](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l4/sprint-l4-full-simulation-story.md)
[^11]: [Technical Documentation - Sprint L4 Story](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l4/sprint-l4-full-simulation-story.md)
[^12]: [Technical Documentation - Sprint L4 Story](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l4/sprint-l4-full-simulation-story.md)
[^13]: [Technical Documentation - Sprint L4 Story](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l4/sprint-l4-full-simulation-story.md)
[^14]: [Technical Documentation - Sprint L4 Story](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l4/sprint-l4-full-simulation-story.md)
[^15]: [Backlog Documentation](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/backlog.md)
[^16]: [Sprint L3 Plan](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/sprint-plan-l3-step-gltf-integration-and-cad-detailing.md)
[^17]: [Backlog Documentation](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/backlog.md)
[^18]: [Sprint L3 Plan](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/sprint-plan-l3-step-gltf-integration-and-cad-detailing.md)
[^19]: [Sprint L3 Plan](https://raw.githubusercontent.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/main/project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/sprint-plan-l3-step-gltf-integration-and-cad-detailing.md)
