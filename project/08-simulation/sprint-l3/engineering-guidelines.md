# Engineering Guidelines for Sprint L3 Simulation

After evaluating the Sprint-L3 review and the technical documents, a clear implementation plan can be derived. The following engineering tasks are necessary for the simulation to achieve realistic detail and configurability:

## 1 Expand Data Model and Parameters

* **New classes in the data model**:
  * `Corridor` (deck, width, positions/segments) – represents tangential walkways; they are based on the walkways and conveyors mentioned in the technical design.
  * `WindowFrame` (window ID, frame thickness, material) – required to model window frames separately; material can be set to aluminum oxide/ALON from the window specification.
  * `EmergencyExit` (deck, opening, position, dimensions) – for the maintenance and emergency openings that must be placed in the hull.
* **Optional parameters in `SphereDeckCalculator`**:
  * `corridors_per_deck: int` (default 2) to specify the number of tangential corridors.
  * `corridor_width: float` for the width of the walkways (e.g., 2 m).
  * `window_frame_thickness: float` (e.g., 0.15 m) for frame thickness.
  * `num_emergency_exits: int` (e.g., 2 per deck) for maintenance/emergency openings.
  * keep existing parameters such as `supports_per_deck` and `num_docking_ports`.

These parameters should be implemented as optional fields with sensible default values so that existing models remain unchanged.

## 2 Adjust Geometry Calculations

* **Corridor geometries**:
  * Determine the radius of each deck (inner radius + deck thickness). Tangential corridors run at this radius and have a defined width; they are modeled as ring segments with gaps for elevator shafts and rooms. The number of corridors results from `corridors_per_deck`, positions are evenly distributed over 360°.
  * For simulations with conveyor belts, additionally generate rectangular cross-sections (0.5 m high) along the corridor.

* **Window frames**:
  * The function `calculate_window_geometry` already creates a cutout for each window; extend it with an additional extrusion outward by `window_frame_thickness`.
  * The frame material is aluminum oxide or ALON according to the window specification; plan a dark color with high metallicity in the glTF exporter.

* **Emergency exit openings**:
  * Implement a method `calculate_emergency_exit_positions` similar to the docking port positions: choose `num_emergency_exits` equidistant angles per deck; the openings are modeled as cylindrical or rectangular shafts in the hull with a defined diameter (e.g., 1.5 m).
  * Emergency exits are equipped with airlocks; this can be represented by an additional ring-shaped frame or bulkhead.

* **Material assignment**: Assign the materials from `specification-and-selected-materials.md` to the components:
  * **Load-bearing structures and supports**: SiC composite.
  * **Hull and heat exchanger**: silane-modified polyimides.
  * **Radial supports**: SiC + carbon fiber reinforced polymers.
  * **Corridors/tangential constructions**: silicone-based elastomers and lightweight carbon polymers.
  * **Windows**: multilayer combination of aluminum oxide/ALON, fused quartz, polycarbonate, and borosilicate glass.

* **Bug fix**: In the STEP exporter, access the material of the respective `Window` instance instead of `win.material` (e.g., `window.material`), because the CadQuery solid does not have a material property.

## 3 Extend Exporters

* **STEP exporter**:
  * For every new element (corridor, window frame, emergency exit, docking port, support) create a separate B-Rep body and store it in the assembly with the associated material.
  * Materials are assigned via the new `Material` class; it's important to store the material metadata as `Application_property` in the STEP export.

* **glTF exporter**:
  * Implement mesh generators for corridors, frames, and emergency exits. Each object type receives its own node with a unique name and PBR material.
  * Use PBR parameters (BaseColorFactor, MetallicFactor, RoughnessFactor) according to the material list; example: SiC = dark gray, metallic, rough surface; ALON = light blue, high transparency, high hardness.
  * Add animation samplers for each movable part (docking port cap, possibly emergency exit door). A simple keyframe approach: keyframes at t=0 (closed) and t=1 s (open), rotational quaternions define the opening. For rotating decks: one node per deck with local rotation animation.

* **Naming convention**: Nodes and meshes should be named logically (`Deck05_Corridor01`, `Deck12_WindowFrame03`, `Hull_EmergencyExit02`) so Blender users can identify them easily.

## 4 Develop Tests

Implement new unit tests in `tests/test_geometry_details.py` and `tests/test_exporter_details.py`:

* **Geometry tests**: Given parameters, the calculated number of corridors, window frames, and emergency exits must be correct; placement should lie within the decks (check radius).
* **Material tests**: Ensure objects receive the correct material from the data model. Check, e.g., that window meshes use ALON material and corridors use elastomer material.
* **Exporter tests**: Load the generated glTF file (e.g., with `pygltflib`) and verify that the number of mesh nodes matches expectations and that animation channels exist for docking ports and deck rotation.
* **Regression tests**: Ensure existing geometries (decks, wormhole, base rings) continue to function unchanged.

## 5 Blender Example Scene and Documentation

* **Example `.blend` file**: Create a scene (e.g., via a Python script `blender_example_scene.py`) that imports the exported glTF model, assigns materials, and defines camera and lighting configuration. This serves as a template for presentations.
* **Documentation**: A Markdown guide `documents/blender-usage.md` should explain step by step how to import the glTF into Blender, how to swap materials, show/hide layers, and play the new animations. Include screenshots and notes on render settings (Cycles vs. Eevee).

## 6 Further Recommendations for the Simulation

The research collection emphasizes that tangential corridors, conveyor belts, and hover channels are essential for internal logistics. Consider these as optional modules to be added in later sprints. Room layouts for medical facilities, hydroponic gardens, recreation areas, and emergency pods should also be prepared in the long term.

These tasks will make the simulation not only more detailed but also configurable and testable. Assigning materials according to the specification and complying with safety and energy systems ensures a believable reproduction of the Earth-ONE station.
