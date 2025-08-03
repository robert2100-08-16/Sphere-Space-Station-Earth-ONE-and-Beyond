# Blender Hull Simulation

This folder contains a minimal Blender Python script that generates a simple hull model for the Sphere Station. It mirrors the approach of the deck simulation but focuses solely on the outer hull.

* **adapter.py** – Creates a basic hull based on `deck_3d_construction_data.csv`.
* **starter.py** – Convenience launcher that starts Blender using the environment variable `BLENDER_PATH`.

`starter.py` can additionally export the station geometry using the bundled CSV:

```bash
python starter.py --export-step hull.step --export-gltf hull.gltf --export-json hull.json
```
