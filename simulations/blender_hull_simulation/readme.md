# Blender Hull Simulation

This folder contains a minimal Blender Python script that imports a hull model
for the Sphere Station.  The geometry is exported beforehand by
``gltf_exporter.py`` and stored as a glTF/GLB file which is then loaded into
Blender.

* **adapter.py** – Imports ``station.glb`` and assigns a grey material to all
  meshes.
* **starter.py** – Convenience launcher that starts Blender using the
  environment variable ``BLENDER_PATH`` and can generate the ``station.glb``
  file via ``--export-gltf``.

Example workflow:

```bash
# 1) Create glTF geometry
python starter.py --export-gltf station.glb

# 2) Open the glTF file in Blender and assign materials
blender --python adapter.py
```
