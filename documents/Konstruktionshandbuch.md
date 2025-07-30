# Konstruktionshandbuch

Dieses Handbuch sammelt wichtige Entscheidungen zur Modellierung der Sphere Space Station und dient als fortlaufende Dokumentation.

## Aktueller Stand

- **Deckdaten** basieren auf den Berechnungen aus `deck_calculations_script.py` und werden für Blender in `deck_3d_construction_data.csv` aufbereitet.
- **Variablennamen** wurden auf ein konsistentes, PEP8‑konformes Schema umgestellt (z.B. `deck_id`, `inner_radius_m`).
- **Blender-Skripte** erzeugen realistisch proportionierte Decks und ein zentrales Wurmloch. Materialien und Fenster werden anhand der CSV‑Daten gesetzt.
- **Realistische Simulation**: Das Blender-Skript weist nun Materialien zu, platziert Fenster automatisch und fügt Energie- sowie Thermalsysteme wie Radiatoren, SMR und Solararrays hinzu. Lichtquellen orientieren sich an Deckfunktionen.

Weitere Anpassungen und Releases werden in diesem Dokument ergänzt.
