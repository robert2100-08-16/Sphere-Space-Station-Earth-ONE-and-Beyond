# Blender Simulation

This folder contains the proof-of-concept Blender files for visualizing the Sphere Station decks.

* **blender_deck_simulation.py** – Blender Python script that builds ring segments from `deck_3d_construction_data.csv`.
* **deck_3d_construction_data.csv** – Geometry values derived from the deck calculations.
* **Blender Simulation Projektplan.docx** (in `../project`) – high-level plan describing data structure and further work.
* **Blender Simulation Sprintplan.docx** – sprint tasks for setting up this folder.

To run the script in Blender:

1. Open Blender (version ≥ 2.9) and switch to the *Scripting* workspace.
2. Load `blender_deck_simulation.py`, adjust the CSV path if necessary and press `Alt+P`.
3. The generated objects appear under `SphereDeckCollection`.

The script can also be executed from the command line:

```
blender --python simulations/blender_simulation/blender_deck_simulation.py --background
```

This will create a `.blend` file in background mode for further processing.
