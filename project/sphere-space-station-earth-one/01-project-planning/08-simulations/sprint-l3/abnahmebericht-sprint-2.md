# Abnahmebericht Sprint 2 (13.10.2025 – 24.10.2025)

## Ziele

1. STEP- und glTF-Exporter unterstützen die vollständige Stationsgeometrie.
2. CSV als Transportformat wurde abgeschafft und nur noch für Berichte genutzt.
3. Blender-Adapter importiert die Geometrie aus glTF.

## Ergebnisse

- `adapters/step_exporter.py`, `gltf_exporter.py` und `json_exporter.py` schreiben vollständige Modelle.
- `blender_hull_simulation` nutzt glTF-Import; die Datei `deck_3d_construction_data.csv` entfällt.
- `starter.py` bietet CLI-Optionen `--export-step`, `--export-gltf` und `--export-json`.
- Reporting-Funktion `to_csv` bleibt für tabellarische Auswertungen erhalten.

## Tests

- Exporter und Blender-Adapter durch automatische Tests geprüft.

