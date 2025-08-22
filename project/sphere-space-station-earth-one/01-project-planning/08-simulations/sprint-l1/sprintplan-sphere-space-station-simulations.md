---
id: ""
title: ""
version: v0.0.0
state: DRAFT
evolution: ""
discipline: ""
system: []
system_id: []
seq: []
owner: ""
reviewers: []
source_of_truth: false
supersedes: null
superseded_by: null
rfc_links: []
adr_links: []
cr_links: []
date: 1970-01-01
lang: EN
---

# 1. Sprintplan: sphere-space-station-simulations


Dieser Plan beschreibt die nächsten Sprints, um die `sphere-space-station-simulations` zu einer vollwertigen Python-Bibliothek auszubauen. Die Ziele sind:

- **Zentralisierung der Logik**: Alle Berechnungen, Animationen, Datenreports und Datenaufbereitungen in einem Rich-Python-Modul bündeln.
- **Saubere CLI-Starter**: Jedes Starter-Skript ruft nur noch die Bibliothek auf.
- **Klarer Ordneraufbau**: 
```

simulations/
├── sphere\_space\_station\_simulations/
├── deck\_calculator/
├── blender\_deck\_simulator/
├── blender\_hull\_simulation/
└── blender\_station\_simulator/

```

---

## 1.1 Sprint 1 (04.08.2025 – 15.08.2025): Bibliothek aufbauen und Kalkulationen migrieren

### 1.1.1 Aufgaben
- `sphere_space_station_simulations`-Paketstruktur anlegen mit `geometry/`, `reporting/`, `animation/`.
- `SphereDeckCalculator` nach `geometry/deck.py` verschieben.
- Reporting- und Animationsfunktionen in eigene Module (`reporting/`, `animation/`) auslagern.
- Unit-Tests aufbauen (z. B. Anzahl Decks, Radien, Volumina).
- Starter/Adapter so anpassen, dass nur noch die Bibliothek importiert wird.

### 1.1.2 Aufgabenübersicht

| Aufgabe                                        | Zielordner/Modul                  | Fälligkeit     |
|-----------------------------------------------|-----------------------------------|----------------|
| Paketstruktur anlegen                         | `simulations/`                    | 05.08.2025     |
| DeckCalculator verschieben                    | `geometry/deck.py`                | 07.08.2025     |
| Reporting-/Animations-APIs extrahieren        | `reporting/`, `animation/`        | 12.08.2025     |
| Starter/Adapter umstellen                     | `deck_calculator/`                | 15.08.2025     |
| Tests schreiben                                | `simulations/tests`               | 15.08.2025     |

---

## 1.2 Sprint 2 (18.08.2025 – 29.08.2025): Blender-Deck-Simulation integrieren

### 1.2.1 Aufgaben
- Funktion `generate_deck_construction_csv()` in `data_preparation.py` integrieren.
- Blender-spezifische Adapterfunktionen in `blender_helpers/` auslagern.
- Starter-Skript `blender_deck_simulator/starter.py` anpassen.
- Tests zur CSV-Generierung und Adapterlaufzeit ergänzen.

### 1.2.2 Aufgabenübersicht

| Aufgabe                                         | Zielordner/Modul                  | Fälligkeit     |
|------------------------------------------------|-----------------------------------|----------------|
| `generate_deck_construction_csv()` integrieren | `data_preparation.py`            | 20.08.2025     |
| Blender-Hilfsfunktionen auslagern              | `blender_helpers/`               | 24.08.2025     |
| Starter anbinden                               | `blender_deck_simulator/`        | 27.08.2025     |
| CSV-/Adapter-Tests                              | `simulations/tests`              | 29.08.2025     |

---

## 1.3 Sprint 3 (01.09.2025 – 12.09.2025): Hull- und Stations-Simulation konsolidieren

### 1.3.1 Aufgaben
- Hüllengeometrie in `geometry/hull.py` migrieren.
- `StationSimulation`-Klasse in `simulation.py` überführen.
- CLI-Starter (`blender_hull_simulation`, `blender_station_simulator`) vereinheitlichen.
- Automatisierte Tests für Hull-/Stationslogik schreiben.

### 1.3.2 Aufgabenübersicht

| Aufgabe                                  | Zielordner/Modul                         | Fälligkeit     |
|------------------------------------------|------------------------------------------|----------------|
| Hull-Funktion migrieren                  | `geometry/hull.py`                       | 03.09.2025     |
| StationSimulation integrieren            | `simulation.py`                          | 06.09.2025     |
| CLI-Starter anpassen                     | `blender_hull_simulation/`, `blender_station_simulator/` | 10.09.2025     |
| Hull-/Stations-Tests                     | `simulations/tests`                      | 12.09.2025     |

---

## 1.4 Sprint 4 (15.09.2025 – 26.09.2025): Dokumentation und Packaging

### 1.4.1 Aufgaben
- README zweisprachig (DE/EN) erstellen.
- `pyproject.toml` bzw. `setup.py` schreiben, CI optional hinzufügen.
- Veraltete Skripte entfernen oder durch Importe ersetzen.

### 1.4.2 Aufgabenübersicht

| Aufgabe                        | Zielordner/Modul             | Fälligkeit     |
|--------------------------------|------------------------------|----------------|
| README/Docs erstellen          | `simulations/`               | 18.09.2025     |
| Paketdateien anlegen          | Projekt-Wurzel               | 22.09.2025     |
| CI-Workflow (optional)         | `.github/workflows/`         | 24.09.2025     |
| Aufräumen alter Skripte        | Starter-Verzeichnisse        | 26.09.2025     |

---

## 1.5 Hinweise

- **Bibliotheksprinzip**: Starter enthalten keine Berechnungslogik mehr.
- **Testpflicht**: Jede Funktion ist mit Unit-Tests abzusichern.
- **Zweisprachigkeit**: Dokumentation auf Deutsch & Englisch. Modulnamen englisch.

---

## 1.6 GitHub-Verweise

- [`deck_calculator.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/deck_calculator.py)
- [`starter.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/deck_calculator/starter.py)
- [`adapter.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/deck_calculator/adapter.py)
- [`generate_3d_construction_csv.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/blender_deck_simulator/generate_3d_construction_csv.py)
- [`station_simulation.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/deck_calculator/station_simulation.py)

