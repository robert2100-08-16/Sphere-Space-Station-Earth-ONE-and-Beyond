# 1. Blender Hull Simulation

This folder contains a minimal Blender Python script that imports a hull model
for the Sphere Station.  The geometry is exported beforehand by
``gltf_exporter.py`` and stored as a glTF/GLB file which is then loaded into
Blender.

* **prepare_blender_scene.py** – located in ``sphere_space_station_simulations``,
  generates ``station.glb`` (and optional STEP or JSON files) using the shared
  exporters.
* **adapter.py** – Imports ``station.glb`` and assigns a grey material to all
  meshes.  If the GLB file is missing, it is created automatically.
* **starter.py** – Convenience launcher that starts Blender using the
  environment variable ``BLENDER_PATH`` and can still generate the
  ``station.glb`` file via ``--export-gltf``.

Example workflow:

```bash
# 1) Run Blender; the adapter prepares the scene if necessary
blender --python adapter.py

# Optionally generate exports without launching Blender
blender --python adapter.py -- --prepare
```
