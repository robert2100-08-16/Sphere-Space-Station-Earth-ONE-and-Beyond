# Konstruktionshandbuch

Dieses Handbuch sammelt wichtige Entscheidungen zur Modellierung der Sphere Space Station und dient als fortlaufende Dokumentation.

## Aktueller Stand

- **Deckdaten** basieren auf den Berechnungen aus `deck_calculations_script.py` und werden für Blender in `deck_3d_construction_data.csv` aufbereitet.
- **Variablennamen** wurden auf ein konsistentes, PEP8‑konformes Schema umgestellt (z.B. `deck_id`, `inner_radius_m`).
- **Blender-Skripte** erzeugen realistisch proportionierte Decks und ein zentrales Wurmloch. Materialien und Fenster werden anhand der CSV‑Daten gesetzt.
- **Realistische Simulation**: Das Blender-Skript weist nun Materialien zu, platziert Fenster automatisch und fügt Energie- sowie Thermalsysteme wie Radiatoren, SMR und Solararrays hinzu. Lichtquellen orientieren sich an Deckfunktionen.
- **Beschleunigungsvisualisierung**: Beim Erzeugen der Decks wird die Farbe nun aus der Zentrifugalbeschleunigung berechnet (0 m/s² → Weiß, 9.81 m/s² → Grün, höhere Werte verlaufen Richtung Rot).
- **Bequemer Start**: `starter.py` startet Blender über die Umgebungsvariable `BLENDER_PATH`. Eine VS-Code-Launch-Konfiguration vereinfacht den Aufruf.
- **Hüllensimulation**: Ein weiteres Skript `adapter.py` erzeugt eine vereinfachte Außenhülle. Über einen eigenen VS‑Code-Starteintrag kann das Skript bequem getestet werden.
- **CSV-Generator** `generate_deck_construction_csv` ist nun Teil der Bibliothek `data_preparation.py` und wird von `generate_3d_construction_csv.py` verwendet.
- **Blender-Hilfsfunktionen** befinden sich im neuen Unterpaket `blender_helpers` und werden vom Adapter importiert.
- **Hüllengeometrie** wird jetzt durch `geometry/hull.py` berechnet und von der
  Deck-Logik importiert.
- **Stationssimulation** ist in `simulation.py` umgezogen und kann direkt aus der
  Bibliothek gestartet werden. `run_simulation.py` heißt nun `starter.py`.

- **Importpfad**: `adapter.py` fügt das Repository-Root dem `sys.path` hinzu,
  wodurch Blender die Hilfsfunktionen korrekt findet.

- **Abhängigkeiten reduziert**: `generate_deck_construction_csv` kommt ohne Pandas aus und das Paket nutzt Lazy‑Imports, sodass die Blender‑Adapter ohne zusätzliche Bibliotheken laufen.
- **Hull-Starter**: `starter.py` der Hüllensimulation verweist nun standardmäßig auf `adapter.py`.

- **Deck-Rendering**: `create_ring_deck` entfernt nur noch die innere Hilfsgeometrie,
  sodass alle Decks statt nur des Wurmlochs erscheinen. Die Deck-ID wird
  nun anhand des Unterstrichs korrekt ausgewertet, damit Fenster für die ersten
  zwölf Decks erzeugt werden.


- **Schichtmodell**: KERNEL, ADAPTER und GUI wurden als klare Ebenen definiert.
- **Datenmodell**: Dataclasses für Decks und Hülle ermöglichen den Export.
- **Prototyp-Exporter**: Erste STEP- und glTF-Dateien werden aus den Datenobjekten generiert.

- **CLI-Exporter**: Starter-Skripte unterstützen nun `--export-step`, `--export-gltf` und `--export-json` zum Ablegen von Geometrie-Dateien; CSV bleibt als Reporting-Ausgabe.

- **Detailreiches Datenmodell**: `Deck` und `Hull` enthalten Netto-Radien,
  Zylinderlängen, Basisflächen sowie Volumina und unterstützen verschachtelte
  Fensterangaben (Position, Größe, Anzahl).

Weitere Anpassungen und Releases werden in diesem Dokument ergänzt.
