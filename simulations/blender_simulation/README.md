# Blender-Simulation

Dieser Ordner enthält die Proof-of-Concept-Dateien für Blender, mit denen die Decks der Sphere Station visualisiert werden.

* **blender_deck_simulation.py** – Blender-Python-Skript, das Ringsegmente aus `deck_3d_construction_data.csv` erzeugt.
* **generate_3d_construction_csv.py** – erzeugt `deck_3d_construction_data.csv` aus `../results/deck_dimensions.csv`.
* **deck_3d_construction_data.csv** – Geometriewerte aus den Deck-Berechnungen.
* **Blender Simulation Projektplan.docx** (in `../project`) – Grobplan mit weiteren Arbeitsschritten.
* **Blender Simulation Sprintplan.docx** – Aufgabenübersicht zum Aufsetzen dieses Verzeichnisses.

## CSV-Spalten

`deck_3d_construction_data.csv` enthält folgende Spalten:

| Spalte | Bedeutung |
|-------|-----------|
| `deck_id` | Name bzw. Nummer des Decks |
| `deck_usage` | vorgesehene Nutzung |
| `inner_radius_m` | Abstand vom Mittelpunkt bis zur inneren Deckwand |
| `outer_radius_m` | Abstand bis zur äußeren Deckwand |
| `outer_radius_netto_m` | nutzbarer Außenradius nach Abzug des Hüllmaterials |
| `deck_height_m` | Gesamthöhe des Decks (brutto) |
| `deck_inner_height_m` | nutzbare Innenhöhe |
| `num_windows` | Anzahl der Fenster |
| `window_material` | verwendetes Fenstermaterial |
| `window_thickness_cm` | Gesamtdicke der Fenster in Zentimetern |
| `structure_material` | Baumaterial des Decks |
| `rotation_velocity_mps` | Umfangsgeschwindigkeit am nutzbaren Außenradius |
| `centrifugal_acceleration_mps2` | Zentrifugalbeschleunigung am nutzbaren Außenradius |

## Generierung der CSV-Datei

Vor dem Start der Blender-Simulation muss `deck_3d_construction_data.csv` erzeugt werden. Das Skript liest die Ergebnisse der Deckberechnung und ergänzt weitere Spalten.

```bash
python simulations/blender_simulation/generate_3d_construction_csv.py
```

Die Datei `deck_3d_construction_data.csv` wird anschließend in diesem Verzeichnis abgelegt.

## Ausführen in Blender

1. Blender (Version ≥ 2.9) starten und in den Arbeitsbereich **Scripting** wechseln.
2. `blender_deck_simulation.py` laden, den Pfad zur CSV-Datei bei Bedarf anpassen und mit `Alt+P` ausführen.
3. Die erzeugten Objekte erscheinen in der Sammlung `SphereDeckCollection`.

## Ausführen über die Kommandozeile

```bash
blender --python simulations/blender_simulation/blender_deck_simulation.py --background
```

Der Befehl erzeugt eine `.blend`‑Datei im Hintergrundmodus zur Weiterverarbeitung.
