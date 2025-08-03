# 1. Deck Calculator

This directory contains the `deck_calculations_script.py` compatibility module together with a simple adapter and starter used to run the calculations.

The script calculates deck geometry, window placement, and hull properties of the Sphere Station.

The `starter.py` exposes a small CLI. In addition to the default CSV report it can export the geometry model:

```bash
python starter.py --export-step station.step --export-gltf station.gltf --export-json station.json
```

CSV output is intended for reporting only.

## 1.1 License

The code here is released under the MIT license to encourage educational use. See `../LICENSE-MIT` for the full text.
