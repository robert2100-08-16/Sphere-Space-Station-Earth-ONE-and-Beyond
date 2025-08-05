# 1. Architecture Documentation

Dieses Verzeichnis bündelt Unterlagen zum Schichtenmodell des Projekts. Das
Modell trennt eine **KERNEL**-Schicht für Berechnungen, **ADAPTER** zur
Formatumwandlung und **GUI**-Schichten für die Visualisierung.

## 1.1 Übersicht

| Dokument | Zweck | Speicherort |
| --- | --- | --- |
| [layered-architecture.md](layered-architecture.md) | Erläutert das Schichtenmodell | simulations/docs/architecture/layered-architecture.md |
| [library-evaluation.md](library-evaluation.md) | Vergleich von STEP- und glTF-Bibliotheken | simulations/docs/architecture/library-evaluation.md |
| [data-model.md](data-model.md) | Dokumentation des Datenmodells (`Deck`, `Hull`, `Wormhole`, `StationModel`) | simulations/docs/architecture/data-model.md |

## 1.2 Exporter und Datenflüsse

Die KERNEL-Schicht liefert strukturierte Geometrie, die über Adapter in
verschiedene Formate überführt wird:

- [`gltf_exporter.py`](../../sphere_space_station_simulations/adapters/gltf_exporter.py)
  erzeugt `station.glb` für die Blender-Importe.
- [`step_exporter.py`](../../sphere_space_station_simulations/adapters/step_exporter.py)
  schreibt `station.step` für CAD‑Workflows.
- [`json_exporter.py`](../../sphere_space_station_simulations/adapters/json_exporter.py)
  serialisiert das komplette Datenmodell.

Blender‑Adapter laden ausschließlich glTF-Dateien. Der frühere
CSV-Transport (`deck_3d_construction_data.csv`) wurde entfernt und CSV bleibt
nur für tabellarische Reports wie `results/deck_dimensions.csv` erhalten.
