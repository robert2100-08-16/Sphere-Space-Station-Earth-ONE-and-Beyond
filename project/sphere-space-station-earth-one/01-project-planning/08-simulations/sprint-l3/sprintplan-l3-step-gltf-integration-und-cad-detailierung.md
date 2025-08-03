# 1. Sprintplan für Simulationen

## 1.1 Sprintplan L3: STEP-/glTF-Integration & CAD-Detailierung

Dieser Sprintplan beschreibt, wie die beiden großen Themen
(1) Umstellung der Simulationen und Animationen auf STEP und glTF sowie
(2) Verfeinerung der CAD-Modelle in den nächsten Monaten umgesetzt
werden. Er baut auf den vorhandenen Simulationen und der Bibliotheksstruktur der
sphere\_space\_station\_simulations auf und führt sie zu einer zukunftsfähigen, schichtbasierten
Architektur (KERNEL → ADAPTER → GUI) weiter. Die vorgeschlagenen Sprints orientieren sich an
zweiwöchigen Iterationen mit klaren Aufgaben, Terminen und Deliverables.

### 1.1.1 Gesamtziele

* **CAD-Austauschformat vereinheitlichen:**
  Die gesamte Geometrie (Decks, Hülle, Fenster, etc.) wird mithilfe eines einzigen präzisen CAD-Formats generiert. Aufgrund seiner Herstellerunabhängigkeit und Präzision wird STEP (ISO 10303) als Kernformat gewählt. Mathematische Geometrien (Volumenkörper) lassen sich damit genau und verlustfrei austauschen.
* **Animations- und Visualisierungsformat vereinheitlichen:**
  Für bewegte Szenen und interaktive Präsentationen wird glTF (alternativ USD) als primäres Animationsformat eingeführt. Es ist offen, webbasiert, effizient und lässt sich aus Python heraus generieren.
* **Sauberer Schichtenaufbau:**
  Die Berechnungslogik bleibt im KERNEL (bisher `geometry/`, `reporting/`, `animation/`); neue ADAPTER erzeugen STEP, glTF, JSON oder andere DTOs; GUI-Schichten (z. B. Blender-Skripte, Web-Viewer, MATLAB-Plots) lesen ausschließlich aus diesen Adapter-Schnittstellen.
* **Feindetaillierte CAD-Modelle:**
  Decks, Hülle, Fenster, Korridore, Docking-Ports, Versorgungsleitungen, etc. werden geometrisch erweitert. Damit entstehen reifere Modelle, die für Fertigung, Simulation und Öffentlichkeitsarbeit geeignet sind.
* **CSV deklassieren:**
  Die bisher genutzten CSV-Dateien zum Geometrie-Transport (z. B. `deck_3d_construction_data.csv` im Blender-Adapter) werden abgelöst. CSV bleibt optional für Berichte (Reporting), während strukturierte Daten via JSON/DTO und STEP/glTF transportiert werden.

Die Sprints starten nach Abschluss des bestehenden Bibliotheksaufbaus (Sprintplan „sphere-space-station-simulations“, letzter Termin 26.09.2025). Die neuen Arbeiten beginnen am 29.09.2025.

---

## 1.2 Sprint 1 (29.09.2025 – 10.10.2025): Architekturentwurf & Technologieauswahl

### 1.2.1 Ziele

1. Tragfähige Architektur für STEP-/glTF-Integration entwerfen.
2. Bibliotheken für STEP- und glTF-Erzeugung evaluieren und auswählen.
3. Erste Prototypen zur Ausgabe von STEP- und glTF-Dateien aus vorhandenen Geometriedaten erstellen.

### 1.2.2 Aufgaben

| Aufgabe                                                                                                                                                                                                                                                                                 | Zielordner/Modul                                                         | Fälligkeit |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------- |
| Bibliotheks-Research: Python-Bibliotheken zur STEP-Erzeugung (z. B. pythonocc-core, cadquery) und glTF (z. B. pygltflib, trimesh) evaluieren. Kriterien: Lizenz, API-Stabilität, Funktionsumfang, Integration mit Numpy/Pandas.                                                         | `docs/architecture/`                                                     | 01.10.2025 |
| Schichtmodell definieren: Dokument erstellen, das die KERNEL-, ADAPTER- und GUI-Schicht klar beschreibt. KERNEL enthält Klassen wie SphereDeckCalculator; ADAPTER enthält Exporter (STEP, glTF, JSON, HTML, CSV) und Importer; GUI umfasst Blender-Skripte, Web-Viewer, MATLAB-Skripte. | `docs/architecture/`                                                     | 03.10.2025 |
| Datenmodell/DTO definieren: Für den Austausch zwischen KERNEL und Adaptern ein einheitliches Datenmodell (z. B. Python-Dataclasses) entwickeln, das Deck- und Hüllengeometrien, Materialien, Bewegungsdaten repräsentiert.                                                              | `simulations/sphere_space_station_simulations/data_model.py`             | 06.10.2025 |
| Prototyp STEP-Exporter: Einen experimentellen Exporter implementieren, der die im KERNEL berechneten Geometrien (Deck-Zylinder und Hülle) in einen STEP-Container schreibt. Nutzung der evaluierten Bibliothek (z. B. pythonocc-core).                                                  | `simulations/sphere_space_station_simulations/adapters/step_exporter.py` | 10.10.2025 |
| Prototyp glTF-Exporter: Analog zum STEP-Exporter eine erste glTF-Ausgabe (Meshes) entwickeln, die Deck- und Hüllendaten in ein glTF-File transformiert. Verwendung z. B. von pygltflib oder trimesh.                                                                                    | `simulations/sphere_space_station_simulations/adapters/gltf_exporter.py` | 10.10.2025 |
| Unit-Tests: Für Datenmodell und Prototyp-Exporter einfache Tests anlegen (Datei wird geschrieben, Dateien lassen sich öffnen).                                                                                                                                                          | `tests/test_adapters.py`                                                 | 10.10.2025 |

### 1.2.3 Deliverables

* Dokumentierte Architektur mit Schichten-Diagramm.
* Evaluationsbericht zu STEP-/glTF-Bibliotheken.
* Grundlegendes Datenmodell (DTOs).
* Erste lauffähige Exporter für STEP und glTF (noch ohne vollumfängliche Geometrie).
* Testabdeckung für Exporter.

---

## 1.3 Sprint 2 (13.10.2025 – 24.10.2025): Adapter ausbauen & CSV ablösen

### 1.3.1 Ziele

1. Vollständige STEP- und glTF-Exporter entwickeln, die alle Geometrien aus dem KERNEL unterstützen (Deck-Zylinder, Hülle inklusive Wurmloch und Basisringe, Fenstergeometrie, Rotationsinformationen).
2. CSV als Transportformat ablösen und nur noch für Berichte nutzen.
3. Bestehende Blender-Adapter auf glTF-Import umstellen.

### 1.3.2 Aufgaben

| Aufgabe                                                                                                                                                                                                                                                  | Zielordner/Modul                                                                           | Fälligkeit |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ---------- |
| STEP-Exporter finalisieren: Den Prototyp erweitern, sodass das gesamte Geometriemodell inkl. Fensterpositionen in STEP geschrieben wird. Material-Placeholder hinzufügen (z. B. Stahl, Glas) als Basis für spätere Rendering-Infos.                      | `adapters/step_exporter.py`                                                                | 16.10.2025 |
| glTF-Exporter finalisieren: Vollständige Mesh-Generierung und Szenenbeschreibung implementieren: Decks als separate Meshes, Hülle, Wurmloch und Basisringe; Fensterlöcher als cut-outs; optionale Animationen (Rotation der Station) als glTF-Animation. | `adapters/gltf_exporter.py`                                                                | 16.10.2025 |
| JSON/DTO-Export: Einen JSON-Exporter entwickeln, der das Datenmodell seriell speichert. Dieses Format dient dem Datenaustausch (z. B. Web-Apps) und wird von den STEP-/glTF-Exportern genutzt.                                                           | `adapters/json_exporter.py`                                                                | 16.10.2025 |
| Blender-Adapter überarbeiten: Die bisherigen Blender-Skripte (`blender_hull_simulation/adapter.py` usw.) entfernen den CSV-Leser und importieren stattdessen das glTF-File. In Blender wird per Python-API glTF geladen und Materialien zugewiesen.      | `simulations/blender_hull_simulation/adapter.py`                                           | 20.10.2025 |
| CSV-Reporting isolieren: Reporting-Funktionen (`reporting/deck.py`) so umbauen, dass CSV nur noch für tabellarische Auswertungen genutzt wird (wie bisher `to_csv`). Das Geometrie-CSV (`deck_3d_construction_data.csv`) wird abgeschafft.               | `reporting/`                                                                               | 20.10.2025 |
| CLI-Starter anpassen: Starter-Skripte (Deck-, Hull- und Station-Simulation) erhalten zusätzliche CLI-Optionen: `--export-step`, `--export-gltf` und `--export-json`, die die jeweiligen Dateien erzeugen. CSV-Option bleibt für Berichte.                | `simulations/deck_calculator/starter.py`, `simulations/blender_hull_simulation/starter.py` | 22.10.2025 |
| Tests erweitern: Prüfen, dass STEP- und glTF-Dateien alle Geometrien enthalten (z. B. Anzahl der Deck-Meshes entspricht Anzahl Decks, Hülle vorhanden). Überprüfen, dass Blender-Import das glTF korrekt lädt.                                           | `tests/test_exporters.py`                                                                  | 24.10.2025 |

### 1.3.3 Deliverables

* Voll funktionsfähige STEP- und glTF-Exporter.
* JSON-Datenformat und Exporter.
* Blender-Adapter, der glTF importiert.
* CLI-Optionen zur Dateiausgabe.
* Erweiterte Testabdeckung (Exporters & Adapter).

---

## 1.4 Sprint 3 (27.10.2025 – 07.11.2025): CAD-Detailtiefe erhöhen

### 1.4.1 Ziele

1. Die CAD-Modelle sollen reichhaltiger und detailgetreuer werden: Decks mit Deckenelementen, Stützen, Korridoren; Hülle mit strukturellen Versteifungen, Wartungsschleusen und Docking-Ports; Fenster mit Rahmen und eventueller Glasstärke.
2. Simulationen sollen optionale Parameter für diese Details aufnehmen können (z. B. Anzahl der Stützen pro Deck, Durchmesser der Docking-Ports).
3. Die Exporter müssen diese feinen Geometrien in STEP und glTF korrekt abbilden.

### 1.4.2 Aufgaben

| Aufgabe                                                                                                                                                                                                                                               | Zielordner/Modul                                                          | Fälligkeit |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------- |
| Geometriemodell erweitern: Die Klasse `SphereDeckCalculator` um Parameter für Stützen, Korridore, Fensterrahmen, Notausstiege und Docking-Ports ergänzen. Berechnungen zur Ermittlung der Positionen und Dimensionen implementieren.                  | `geometry/deck.py`, `geometry/hull.py`                                    | 31.10.2025 |
| Material- und Farbeigenschaften: Datenmodell und Exporter um Material- und Farbangaben ergänzen (z. B. Stahl, Aluminium, Glas; Farbe als RGB). Diese Informationen werden beim Export in glTF als PBR-Materialien und in STEP als Metadaten abgelegt. | `data_model.py`, `adapters/gltf_exporter.py`, `adapters/step_exporter.py` | 31.10.2025 |
| Detail-Animationen: Für glTF zusätzliche Animationen implementieren: z. B. Öffnen/Schließen von Docking-Ports, Rotation einzelner Decks für Wartung.                                                                                                  | `adapters/gltf_exporter.py`                                               | 03.11.2025 |
| Prototyp-Visualisierung in Blender: Beispielszene erstellen, die das feindetaillierte Modell mit Materialien importiert und rendert. Dokumentation, wie die glTF-Datei in Blender geladen und weiterverarbeitet wird.                                 | `recommendations/blender_example_scene.blend` (oder Markdown-Dok)         | 07.11.2025 |
| Tests für Details: Unit-Tests hinzufügen, die prüfen, dass z. B. die Zahl der Docking-Ports in STEP der in der Simulation gesetzten entspricht, und dass glTF entsprechende Mesh-Gruppen enthält.                                                     | `tests/test_geometry_details.py`                                          | 07.11.2025 |

### 1.4.3 Deliverables

* Erweiterte Geometrieklassen mit zusätzlichen Parametern.
* STEP- und glTF-Exporter mit Material- und Detailunterstützung.
* Animierte glTF-Beispiele.
* Dokumentierte Blender-Szene und Anleitung.
* Tests für Detailgeometrien.

---

## 1.5 Sprint 4 (10.11.2025 – 21.11.2025): Integration, Dokumentation & Qualitätssicherung

### 1.5.1 Ziele

1. Alle neuen Komponenten zusammenführen und stabilisieren.
2. Umfassende Dokumentation in Deutsch und Englisch erstellen.
3. Automatisierte Qualitätskontrollen und CI einrichten.

### 1.5.2 Aufgaben

| Aufgabe                                                                                                                                                                                                                | Zielordner/Modul            | Fälligkeit |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ---------- |
| Integrationstests: End-to-End-Tests schreiben, die den kompletten Flow abbilden: Geometrie berechnen → Export in STEP/glTF → Import in Blender/Web-Viewer → Rendern/Visualisieren.                                     | `tests/test_integration.py` | 14.11.2025 |
| Dokumentation aktualisieren: README und API-Dokumentation zweisprachig (DE/EN) erweitern; Migrationshinweise zur STEP-/glTF-Umstellung; Beispiele für die Nutzung der neuen CLI-Optionen; Schichtmodell erläutern.     | `README.md`, `docs/`        | 18.11.2025 |
| Refactoring & Aufräumen: Veraltete CSV-Adapter und Skripte entfernen; Namenskonventionen vereinheitlichen; PEP8-Cleanups durchführen.                                                                                  | gesamtes Repository         | 18.11.2025 |
| Continuous Integration (CI): Einen CI-Workflow definieren (GitHub Actions), der Tests für Python, STEP/glTF-Exports und Blender-Skripte ausführt. Optional: automatischer Upload von Artefakten (glTF/STEP-Beispiele). | `.github/workflows/ci.yml`  | 21.11.2025 |
| Stakeholder-Review & Feedback: Ergebnisse (STEP-Datei, glTF-Szene, Rendering) präsentieren. Feedback sammeln (z. B. zu Detailgenauigkeit, Dateigrößen) und Backlog für weitere Iterationen anlegen.                    | `project/backlog.md`        | 21.11.2025 |

### 1.5.3 Deliverables

* Vollständiger STEP-/glTF-Export-Pipeline inkl. automatischer Tests.
* Zweisprachige Dokumentation und Migrationsleitfaden.
* CI-Workflow für die Qualitätskontrolle.
* Bereinigtes Repository ohne veraltete CSV-Skripte.
* Feedback-Protokoll für zukünftige Verbesserungen.

---

## 1.6 Hinweise & Argumentation zur Toolwahl

* **STEP als CAD-Format:**
  Der Kernvorteil von STEP liegt in seiner Präzision und der softwareunabhängigen Beschreibung komplexer Volumenkörper. Während OBJ oder STL einfacher zu erzeugen sind, verlieren sie B-Rep-Informationen; daher wird STEP für die Kerngeometrie verwendet.
* **glTF für Animationen:**
  glTF ist kompakt, webbasiert und von Blender nativ unterstützt. Es erlaubt Material- und Animationsdefinitionen und lässt sich mit Python-Bibliotheken generieren.
* **USD als Option:**
  USD bleibt als Option für sehr große Szenen bestehen, kann aber in einem späteren Sprint evaluiert werden.
* **Klares Schichtenmodell:**
  Die vorhandene Bibliotheksstruktur mit `geometry/`, `reporting/` und `animation/` bildet den Kern (KERNEL). Neue ADAPTER sind verantwortlich für die Übersetzung der berechneten Geometrie in STEP/glTF/JSON/CSV und lösen die bisher direkte Kopplung (z. B. CSV-Leser in Blender-Skripten). GUI-Schichten wie die Blender-Skripte sollen künftig nur noch auf diese Adapter zugreifen und keine eigene Berechnungslogik enthalten.
* **CSV weiterhin für Berichte:**
  Funktionen wie `to_csv()` bleiben als Reporting-Werkzeug erhalten, werden aber nicht mehr zum Geometrie-Transport verwendet. Die Umstellung auf strukturierte DTOs und STEP/glTF reduziert Mehrfachimplementierungen und erhöht die Konsistenz.

---

## 1.7 Fußnoten

1. [https://chatgpt.com/?utm\_src=deep-research-pdf](https://chatgpt.com/?utm_src=deep-research-pdf)
2. [https://chatgpt.com/?utm\_src=deep-research-pdf](https://chatgpt.com/?utm_src=deep-research-pdf)
3. [https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere\_space\_station\_simulations/README.md#L3-L11](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/README.md#L3-L11)
4. [https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/recommendations/blender\_simulation\_recommendations.md#L10-L24](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/recommendations/blender_simulation_recommendations.md#L10-L24)
5. [https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/blender\_hull\_simulation/adapter.py#L1-L37](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/blender_hull_simulation/adapter.py#L1-L37)
6. [https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere\_space\_station\_simulations/geometry/hull.py#L6-L67](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/geometry/hull.py#L6-L67)
7. [https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere\_space\_station\_simulations/geometry/deck.py#L97-L133](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/geometry/deck.py#L97-L133)
8. [https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere\_space\_station\_simulations/reporting/deck.py#L46-L58](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/reporting/deck.py#L46-L58)
9. [https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/recommendations/blender\_simulation\_recommendations.md](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/recommendations/blender_simulation_recommendations.md)
10. [https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere\_space\_station\_simulations/README.md](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/README.md)
11. [https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/recommendations/blender\_simulation\_recommendations.md#L10-L24](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/recommendations/blender_simulation_recommendations.md#L10-L24)
