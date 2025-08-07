**Evaluation of Sprint 3 (STEP/glTF Integration & CAD detailing)**

The sprint plan for sprint L3 (27 Oct – 07 Nov 2025) clearly defined several goals: expanding the deck/hull geometry with supports, corridors, window frames, emergency exits and docking ports, adding material and colour attributes, implementing detail animations, providing an example Blender scene and extending tests.  During a second review of the repository, the current implementation only partially addresses these requirements.

### What has been delivered

* **New parameters for supports and docking ports:** The simulation engine’s `SphereDeckCalculator` introduces parameters (`supports_per_deck`, `num_docking_ports`, `docking_port_diameter`) and computes locations for supports.  A `Material` data class exists and default materials (“Stahl” and “Glas”) are used.  These additions align with the sprint plan’s requirement to begin adding structural details and materials.
* **Material handling in exporters:** The glTF exporter creates GLTF materials with PBR properties depending on the `Material` name (e.g., metallic/roughness values for steel and glass).  The STEP exporter attaches material metadata to deck/hull/base ring/wormhole solids.
* **Standard material definitions and CLI options:** Predefined materials ("Stahl", "Aluminium", "Glas", "Polymer") with RGBA colours are available in the data model.  The simulation CLI allows choosing deck and hull materials, and exporters include these selections in their outputs.
* **Basic rotation animation:** The glTF exporter still provides the simple rotation animation of the whole station noted in prior sprints.

### Deltas – what is still missing

1. **Geometry for corridors, window frames and emergency exits.**

   * The current data model has no classes or structures for corridors, frames or emergency exits.
   * The `SphereDeckCalculator` only computes support positions; there is no geometry for supports or docking ports, and nothing for corridors or emergency exits.
   * **To complete:** define DTOs (e.g., `Corridor`, `WindowFrame`, `EmergencyExit`, `Support`, `DockingPort`) in `data_model.py` with appropriate dimensions and materials; extend `SphereDeckCalculator` to calculate their geometry using CadQuery; integrate these objects into the station model (decks or hull) and attach them to the correct deck/hull positions.  Engineering guidelines specify new parameters such as `corridors_per_deck` (default 2), `corridor_width` ≈ 2 m, `window_frame_thickness` 0.15 m and `num_emergency_exits` 2 per deck【F:project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/engineering-guidelines.md†L5-L15】.  The accompanying engineering brief describes tangential corridors running like ring roads around each deck with optional 0.5 m high conveyors for cargo transport【F:project/sphere-space-station-earth-one/01-project-planning/02-engineering/02-concepts/engineering-to-simulation-l3ff.pdf†L10-L18】.

2. **Exporting the new details.**

   * Neither the glTF exporter nor the STEP exporter references supports, docking ports, corridors, window frames or emergency exits.
   * **To complete:** update `_build_deck_mesh` and `_build_hull_mesh` in the glTF exporter to accept lists of additional solids and window frames, convert them to meshes and assign proper materials.  For the STEP exporter, create helper functions to build B‑Rep solids for each new component and add them to the assembly with the correct metadata.  The engineering guidelines require both exporters to generate separate bodies for corridors, frames, emergency exits and docking ports and to store material metadata in STEP while applying PBR materials and logical node names in glTF【F:project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/engineering-guidelines.md†L43-L55】.

3. **Detail animations.**

   * The current glTF exporter only provides a rotation animation of the entire station; there are no door/hatch animations or moving docking ports.
   * **To complete:** design animations for dynamic parts (opening/closing emergency exits, extending docking ports).  Use glTF animation channels (samplers and channels) to animate translations/rotations of the corresponding nodes.  Provide an API in the data model to define animation sequences and durations.  According to the engineering guidelines, movable parts should use keyframes at t = 0 s (closed) and t = 1 s (open) with quaternions describing the motion and one node per deck for rotation【F:project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/engineering-guidelines.md†L49-L52】.

4. **Blender example scene.**

   * The sprint plan calls for a Blender example of the detailed model with animations, but no `.blend` or instructions are provided.
   * **To complete:** create an example scene in Blender by importing the exported glTF, verify that geometry and animations render correctly, add cameras and lighting, and supply the `.blend` file in the repository.  Document the workflow in a README.  The engineering guidelines recommend shipping a template scene and a `documents/blender-usage.md` guide for import steps and render settings【F:project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/engineering-guidelines.md†L65-L68】.

5. **Testing & CLI integration.**

   * There are currently no tests covering the new geometry or exports.  Existing tests focus on simple placeholder meshes.
   * **To complete:** write unit tests verifying that the new DTOs are created correctly, the `SphereDeckCalculator` generates the expected number and placement of supports, corridors and exits, and that glTF and STEP exporters include these elements with correct materials and animations.  Update CLI scripts to accept parameters for the number of supports/docking ports, corridor widths, etc., and add tests to ensure CLI options work.  Suggested test modules and checks are outlined in the engineering guidelines, including geometry and exporter tests plus regression coverage【F:project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/engineering-guidelines.md†L56-L63】.

6. **Documentation updates.**

   * The sprint plan required updating documentation to describe new features.  The repository’s README and module docstrings still reflect the earlier simplified model.
   * **To complete:** expand the README and module docs to describe the new data classes, CLI options, supported materials, and example usage.  Ensure the sprint‑plan file is updated when tasks are complete.  Include the Blender usage guide mentioned above and reference material assignments from the engineering guidelines to keep docs consistent with the simulation roadmap【F:project/sphere-space-station-earth-one/01-project-planning/08-simulations/sprint-l3/engineering-guidelines.md†L34-L39】.

### Summary and guidance

The current implementation has made progress in adding material classes, CLI material selection and starting support and docking port parameters.  However, most of the sprint‑L3 deliverables remain unfulfilled: there is no corridor, window frame or emergency exit geometry; exporters do not output supports or docking ports; no detail animations or Blender scene exists; tests and documentation are missing.  To close sprint 3, the development team needs to implement the missing data models, compute and export the new geometry, create animations, provide examples and tests, and update documentation as outlined above.
