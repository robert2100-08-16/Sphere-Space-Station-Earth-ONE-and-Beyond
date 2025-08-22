---
title: "Acceptance Report Sprint L3-3"
version: 1.0.1
owner: "Robert Alexander Massinger"
license: "(c) COPYRIGHT 2023 - 2025 by Robert Alexander Massinger, Munich, Germany. ALL RIGHTS RESERVED."
history:
  - version: 1.0.1
    date: 2025-08-06
    change: "Translation to English"
    reference: "abnahmebericht-sprint-3.md"
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

# Acceptance Report Sprint L3-3

During the acceptance of Sprint 3 I compared the sprint plan “STEP/glTF Integration & CAD Detailing” with the actual state in the repository. According to the plan, Sprint 3 aims to further detail the CAD models (decks with ceiling elements, supports, corridors; hull with stiffeners, maintenance hatches and docking ports; windows with frames), introduce optional parameters for these details and adapt the exporters accordingly.

**Completed Points**

| Topic                                         | Implemented Status                                                                                                   | Reference |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------- |
| Parameters for supports & docking ports       | The class `SphereDeckCalculator` now contains optional parameters `supports_per_deck`, `num_docking_ports` and `docking_port_diameter`. When generating the geometry model, a support geometry (`_calculate_support_geometry`) and docking port positions (`calculate_docking_port_positions`) are computed. | Geometry model |
| Materials & colors                            | The data model defines a `Material` class with optional RGBA color. The exporters create standard material instances for steel and glass; the STEP exporter writes material metadata into the B-rep assemblies, and the glTF exporter sets up PBR materials with color, metal and roughness values. | Data model & exporters |
| Basic implementation of docking ports & supports | With the new parameters, additional supports and docking ports can be generated in the script; however, the glTF and STEP exporters do not yet output these elements as separate meshes/bodies. | Geometry model |

**Still Open / Deltas**

| Planned Task                                  | Current State                                                                                                        | How it needs to be implemented |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Corridors, window frames & emergency exits** | Neither `SphereDeckCalculator` nor `geometry/hull.py` contain parameters or calculations for corridors (walkways), window frames or emergency exits. | Extend the model with attributes such as `corridors_per_deck`, `window_frame_thickness`, `num_emergency_exits`; implement functions to compute their positions and dimensions. In `data_model.py` create new DTO classes (e.g., `Corridor`, `Frame`, `EmergencyExit`). |
| **Detail geometries in exporters**            | The STEP/glTF exporters output decks, hull, wormhole and base rings; supports and docking ports are not yet exported. Corridors, window frames and emergency exits are also missing. | The exporters must generate corresponding CAD objects or meshes for each new geometry element. In glTF each type should be exported as a separate mesh group with suitable material. |
| **Material assignment**                       | Materials are assigned only globally per deck/hull. Color coding of different parts (e.g., aluminum vs. steel) is not implemented; in the STEP exporter the material of windows is incorrectly derived from `win.material` although `win` is a CadQuery object. | For each new object class the material should be defined via the DTO. In `step_exporter.py` use the material from the underlying `Window` instance instead of `win.material`. |
| **Detail animations**                         | The glTF exporter only includes a simple rotation of the entire system; animations for opening/closing docking ports or rotating individual decks are missing. | Create animation samplers for each movable component: e.g., docking port caps with two rotation positions and time keys. Individual decks can rotate around their local axis. Embed the animation data (keyframes, quaternions) into the glTF file. |
| **Blender example scene & documentation**     | No `blender_example_scene.blend` or markdown guide exists in the repository; the existing Blender adapter script only imports a glTF file and assigns a basic material. | Provide an example blend file (or `*.py` script) that imports the exported detailed model, assigns materials and shows render settings. In a markdown file, explain how to load the glTF file in Blender, replace materials and play animations. |
| **Tests for details**                         | There is no `tests/test_geometry_details.py`; the existing tests cover only basic functionality. | Write unit tests that check whether the number of generated supports and docking ports matches the configuration, whether window frames and corridors are correctly placed, and whether the glTF exporter creates corresponding mesh groups. The tests should analyze the STEP/glTF files and compare the results with the input parameters. |
| **Minor errors**                              | – The STEP exporter references `win.material` for windows, but `win` is a CadQuery solid without material attribute → error. – The glTF exporter animation rotates only the entire station; parameters for individual animations are missing. | In the STEP exporter use the material name from the `Window` instance (`w.material`). Implement extended animation functions (see above). |

**Conclusion**

From the product owner's perspective, Sprint 3 is not yet complete. Initial extensions have been introduced (support & docking port parameters, material classes), but essential parts of the detail level are still missing, particularly corridors, window frames, emergency exits, differentiated materials, specific animation sequences, an example Blender scene and comprehensive tests. I recommend addressing the deltas listed above in the next iteration, extending the exporters accordingly and providing traceable documentation.

