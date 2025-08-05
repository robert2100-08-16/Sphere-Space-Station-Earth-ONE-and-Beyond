# 1. Blender Deck Simulator

Dieses Verzeichnis enthält die Proof-of-Concept-Dateien für Blender, mit denen
Decks der Sphere Station visualisiert werden. Die Geometrie wird über eine
GLB-Datei bereitgestellt und bei Bedarf automatisch erzeugt.

* **prepare_blender_scene.py** – generiert `station.glb` (optional STEP oder
  JSON) mittels der gemeinsamen Exportfunktionen.
* **adapter.py** – importiert `station.glb` und weist einfachen Materialien zu.
* **starter.py** – Komfortskript zum Starten von Blender über die
  Umgebungsvariable `BLENDER_PATH`; ruft `prepare_scene` auf, um fehlende
  Exportdateien zu erzeugen.

## 1.1 Ausführen in Blender

1. Falls nicht vorhanden, `prepare_blender_scene.py` ausführen, um `station.glb`
   zu erzeugen.
2. Starte Blender (≥ 2.9) und wechsle in den Arbeitsbereich **Scripting**.
3. Lade `adapter.py` und führe das Skript aus (`Alt+P`) oder rufe
   `blender --python adapter.py` auf.

## 1.2 Ausführen mit `starter.py`

Setze die Umgebungsvariable `BLENDER_PATH` auf dein Blender-Executable und
starte anschließend:

```bash
python starter.py --background
```

Weitere Argumente werden direkt an Blender weitergereicht. Über die Parameter
`--export-step`, `--export-gltf` und `--export-json` lassen sich zusätzliche
Dateien erzeugen.
