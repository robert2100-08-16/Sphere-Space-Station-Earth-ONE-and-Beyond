# 1. Blender Deck Simulator

Dieses Verzeichnis enthält die Proof-of-Concept-Dateien für Blender, mit denen
Decks der Sphere Station visualisiert werden. Die Geometrie wird inzwischen
über eine glTF-Datei bereitgestellt; die früher genutzten CSV-Hilfsdateien
entfallen.

* **adapter.py** – importiert `station.glb` und weist einfachen Materialien
  zu.
* **starter.py** – Komfortskript zum Starten von Blender über die
  Umgebungsvariable `BLENDER_PATH`.

## 1.1 Ausführen in Blender

1. Exportiere `station.glb` mit dem glTF-Exporter.
2. Starte Blender (≥ 2.9) und wechsle in den Arbeitsbereich **Scripting**.
3. Lade `adapter.py` und führe das Skript aus (`Alt+P`) oder rufe
   `blender --python adapter.py` auf.

## 1.2 Ausführen mit `starter.py`

Setze die Umgebungsvariable `BLENDER_PATH` auf dein Blender-Executable und
starte anschließend:

```bash
python starter.py --background
```

Weitere Argumente werden direkt an Blender weitergereicht.
