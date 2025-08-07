# 1. Architecture Documentation / Architekturdokumentation

This directory bundles notes about the project's layered model. The model
separates a **KERNEL** layer for calculations, **ADAPTERS** for format
conversion and **GUI** layers for visualisation.

Dieses Verzeichnis bündelt Unterlagen zum Schichtenmodell des Projekts. Das
Modell trennt eine **KERNEL**‑Schicht für Berechnungen, **ADAPTER** zur
Formatumwandlung und **GUI**‑Schichten für die Visualisierung.

## 1.1 Overview / Überblick

| Document | Zweck | Speicherort |
| --- | --- | --- |
| [layered-architecture.md](layered-architecture.md) | Layer model explanation / Erläutert das Schichtenmodell | simulations/docs/architecture/layered-architecture.md |
| [library-evaluation.md](library-evaluation.md) | STEP vs. glTF libraries / Vergleich von STEP- und glTF-Bibliotheken | simulations/docs/architecture/library-evaluation.md |
| [data-model.md](data-model.md) | Data model (`Deck`, `Hull`, `Wormhole`, `StationModel`) / Dokumentation des Datenmodells | simulations/docs/architecture/data-model.md |

## 1.2 Exporters and Data Flow / Exporter und Datenflüsse

The KERNEL layer provides structured geometry which adapters convert into
various formats:

- [`gltf_exporter.py`](../../sphere_space_station_simulations/adapters/gltf_exporter.py)
  writes `station.glb` for Blender imports.
- [`step_exporter.py`](../../sphere_space_station_simulations/adapters/step_exporter.py)
  writes `station.step` for CAD workflows.
- [`json_exporter.py`](../../sphere_space_station_simulations/adapters/json_exporter.py)
  serialises the full data model.

Die KERNEL-Schicht liefert strukturierte Geometrie, die über Adapter in
verschiedene Formate überführt wird:

- [`gltf_exporter.py`](../../sphere_space_station_simulations/adapters/gltf_exporter.py)
  erzeugt `station.glb` für die Blender-Importe.
- [`step_exporter.py`](../../sphere_space_station_simulations/adapters/step_exporter.py)
  schreibt `station.step` für CAD‑Workflows.
- [`json_exporter.py`](../../sphere_space_station_simulations/adapters/json_exporter.py)
  serialisiert das komplette Datenmodell.

Blender adapters import only glTF files. The legacy CSV transport has been
removed; CSV remains only for analytical reports like
`results/deck_dimensions.csv`.

Blender‑Adapter laden ausschließlich glTF-Dateien. Der frühere
CSV-Transport (`deck_3d_construction_data.csv`) wurde entfernt und CSV bleibt
nur für tabellarische Reports wie `results/deck_dimensions.csv` erhalten.

## 1.3 Migration Notes / Migrationshinweise

Use the CLI options `--export-step` and `--export-gltf` to generate geometry
files for the adapters.

Verwenden Sie die CLI‑Optionen `--export-step` und `--export-gltf`, um
Geometriedateien für die Adapter zu erzeugen.
