# Blender-Simulation

Dieser Ordner enthält die Proof-of-Concept-Dateien für Blender, mit denen die Decks der Sphere Station visualisiert werden.

* **blender_deck_simulation.py** – Blender-Python-Skript, das Ringsegmente aus `deck_3d_construction_data.csv` erzeugt.
* **generate_3d_construction_csv.py** – erzeugt `deck_3d_construction_data.csv` aus `../results/deck_dimensions.csv`.
* **deck_3d_construction_data.csv** – Geometriewerte aus den Deck-Berechnungen.
* **blender_starter.py** – Komfortskript zum Starten von Blender über die Umgebungsvariable `BLENDER_PATH`.
* **Blender Simulation Projektplan.docx** (in `../project`) – Grobplan mit weiteren Arbeitsschritten.

* **Blender Simulation Sprintplan.docx** – Aufgabenübersicht zum Aufsetzen dieses Verzeichnisses.

## Beschreibung der Deckdaten

Die Datei `deck_3d_construction_data.csv` wird aus den Ergebnissen des Skriptes
`generate_3d_construction_csv.py` generiert und enthält alle Kenndaten der
einzelnen Decks. Ein **Deck** bezeichnet dabei den Raum zwischen zwei
koaxialen Röhren der Station. Deck **000** bildet ein offenes Wurmloch und ist
nicht mit Atmosphäre befüllt, verfügt aber über Fenster, Schleusen und Docking
Bays in seiner Hülle.

## CSV-Spalten

`deck_3d_construction_data.csv` enthält folgende Spalten:

| Spalte | Bedeutung |
|-------|-----------|
| `deck_id` | Kennung des Decks (`Deck_000` bis `Deck_015`) |
| `deck_usage` | vorgesehene Nutzung |
| `inner_radius_m` | Deckbeginn Radius |
| `outer_radius_m` | Deckende Radius, inkl. Röhrenwand |
| `outer_radius_netto_m` | Deckende Radius ohne Röhrenwand |
| `deck_height_m` | Bruttohöhe des Decks inklusive Röhrenwand |
| `deck_inner_height_m` | nutzbare Deck Innenhöhe |
| `num_windows` | Anzahl der eingeplanten Außenfenster |
| `window_material` | Aufbau des transparenten Materials |
| `window_thickness_cm` | Gesamtdicke des Fensterpakets in Zentimetern |
| `structure_material` | vorgesehenes Konstruktionsmaterial der Deckstruktur |
| `rotation_velocity_mps` | Umfangsgeschwindigkeit am Boden der Röhre |
| `centrifugal_acceleration_mps2` | Zentrifugalbeschleunigung am Boden der Röhre |

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

## Ausführen mit `blender_starter.py`

Setze die Umgebungsvariable `BLENDER_PATH` auf dein Blender-Executable und
starte anschließend:

```bash
python blender_starter.py --background
```

Weitere Argumente werden direkt an Blender weitergereicht.
