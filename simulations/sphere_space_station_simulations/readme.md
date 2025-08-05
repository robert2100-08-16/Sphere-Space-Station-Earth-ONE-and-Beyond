# 1. Sphere Space Station Simulations Library

This package bundles the core calculations, animation helpers and data export functionality used by the example simulations.  It is organised into subpackages:

```
geometry/   - core classes such as ``SphereDeckCalculator``
reporting/  - CSV/HTML export utilities
animation/  - functions producing Matplotlib animations
```

The modules here can be reused by the thin adapters located in the individual simulation folders.

## 1.1 Command Line Interface

The ``simulation.py`` module exposes a small CLI for generating geometry files:

```
python -m simulations.sphere_space_station_simulations.simulation \
    --export-step station.step \
    --export-gltf station.glb \
    --export-json station.json
```

Each flag writes the station model to the respective format.  The exported
glTF file can be imported with the Blender adapters in this repository.  The
CSV geometry helpers have been removed; ``deck_3d_construction_data.csv`` is no
longer produced and JSON/STEP/glTF serve as the interchange formats.
