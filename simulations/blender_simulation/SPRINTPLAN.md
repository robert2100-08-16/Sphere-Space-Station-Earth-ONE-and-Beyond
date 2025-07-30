# CODEX AI Sprint Plan – Implementing the Blender Simulation

## Context

As part of Roadmap EPIC-01 an extensible Blender simulation will be developed. Starting from the existing deck calculations (`deck_calculations_script.py`) and the technical documents of the Sphere Space Station, the goal is to produce a CSV with all relevant 3D construction dimensions. Based on this data a first 3D representation is generated in Blender. The code will be stored in the repository under `simulations/blender_simulation`.

## Objectives

- Create the folder `simulations/blender_simulation` in the existing repository.
- Derive `deck_3d_construction_data.csv` from `simulations/results/deck_dimensions.csv` and add equipment details from the technical documentation.
- Implement a Blender Python script that reads the CSV and generates deck geometries, the central cylinder ("wormhole"), and base rings.
- Document the simulation and how to run it in `README.md`.

## Tasks (User Stories)

| # | Task | Acceptance Criteria |
| --- | --- | --- |
| **1** | **Organize folder** – create the path `simulations/blender_simulation` in the repository with subfiles | Folder exists and initially contains a `.gitkeep` or is empty. |
| **2** | **Generate CSV** – read `simulations/results/deck_dimensions.csv` and derive `deck_3d_construction_data.csv`. Add columns: `deck_usage`, `deck_height_m`, `num_windows`, `window_material`, `window_thickness_cm`, `structure_material`, `rotation_velocity_mps`, `centrifugal_acceleration_mps2` based on the technical documents. | `deck_3d_construction_data.csv` is in the new folder with one row per deck (Deck 000–Deck 015) and consistent values. |
| **3** | **Write Blender script** – implement `blender_deck_simulation.py` that reads the above CSV and performs the following steps: 1. clear the scene; 2. create two cylinders per deck (inner and outer radius), combine them into a ring shell via Boolean and stack along the Z-axis; 3. generate a continuous cylinder as the central passage; 4. add base rings at the top and bottom; 5. move all objects into a collection. | Running the script in Blender shows the decks stacked correctly along with the central cylinder and base rings; no errors occur. |
| **4** | **Create documentation** – write `README.md` in the same folder describing purpose, structure and contents of the CSV, how the script works and how to run it in Blender via GUI or command line. | README exists, written in clear German, describing all relevant steps and referencing the necessary files. |
| **5** | **Test & validate** – open Blender, import the script and CSV, and run the script. Validate that the generated models appear and the dimensions seem plausible (e.g. deck heights and radii). | The simulation runs in Blender without error. The generated geometry matches the input data in spot checks. |

## Schedule / Effort Estimate

| Task | Effort |
| --- | --- |
| Create folder | 0.5 h |
| Derive CSV (including data analysis and additions) | 2 h |
| Develop & test Blender script | 4 h |
| Write documentation | 1 h |
| Integration and final tests | 1.5 h |
| **Total** | **9 h** |

## Implementation Notes

- **Blender version** – development should be done with Blender ≥ 2.9 because the API changed in earlier versions. Only minor adjustments are expected for later Blender versions (3.x).
- **Boolean operations** – the Boolean modifier is applied directly in the script. If a future Blender version causes issues, the `bpy.ops.mesh.boolean_mod()` API can be used instead.
- **Windows & equipment** – the generated decks currently contain no windows or interior. A later extension may use the `windows_count` column with arrays or Booleans to place window openings along the circumference.
- **Performance** – with many decks or higher detail the generation may take several seconds. It is recommended to test the script in background mode (`blender --background --python …`).

## Deliverables

After all tasks are complete the repository should contain:

- `simulations/blender_simulation/deck_3d_construction_data.csv`
- `simulations/blender_simulation/blender_deck_simulation.py`
- `simulations/blender_simulation/README.md`

These files provide the basis for more detailed simulations of the Sphere Space Station in future EPICs.

