# Sprintplan: sphere-space-station-simulations


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

## Sprint 1 (04.08.2025 – 15.08.2025): Bibliothek aufbauen und Kalkulationen migrieren

### Aufgaben
- `sphere_space_station_simulations`-Paketstruktur anlegen mit `geometry/`, `reporting/`, `animation/`.
- `SphereDeckCalculator` nach `geometry/deck.py` verschieben.
- Reporting- und Animationsfunktionen in eigene Module (`reporting/`, `animation/`) auslagern.
- Unit-Tests aufbauen (z. B. Anzahl Decks, Radien, Volumina).
- Starter/Adapter so anpassen, dass nur noch die Bibliothek importiert wird.

### Aufgabenübersicht

| Aufgabe                                        | Zielordner/Modul                  | Fälligkeit     |
|-----------------------------------------------|-----------------------------------|----------------|
| Paketstruktur anlegen                         | `simulations/`                    | 05.08.2025     |
| DeckCalculator verschieben                    | `geometry/deck.py`                | 07.08.2025     |
| Reporting-/Animations-APIs extrahieren        | `reporting/`, `animation/`        | 12.08.2025     |
| Starter/Adapter umstellen                     | `deck_calculator/`                | 15.08.2025     |
| Tests schreiben                                | `simulations/tests`               | 15.08.2025     |

---

## Sprint 2 (18.08.2025 – 29.08.2025): Blender-Deck-Simulation integrieren

### Aufgaben
- Funktion `generate_deck_construction_csv()` in `data_preparation.py` integrieren.
- Blender-spezifische Adapterfunktionen in `blender_helpers/` auslagern.
- Starter-Skript `blender_deck_simulator/starter.py` anpassen.
- Tests zur CSV-Generierung und Adapterlaufzeit ergänzen.

### Aufgabenübersicht

| Aufgabe                                         | Zielordner/Modul                  | Fälligkeit     |
|------------------------------------------------|-----------------------------------|----------------|
| `generate_deck_construction_csv()` integrieren | `data_preparation.py`            | 20.08.2025     |
| Blender-Hilfsfunktionen auslagern              | `blender_helpers/`               | 24.08.2025     |
| Starter anbinden                               | `blender_deck_simulator/`        | 27.08.2025     |
| CSV-/Adapter-Tests                              | `simulations/tests`              | 29.08.2025     |

---

## Sprint 3 (01.09.2025 – 12.09.2025): Hull- und Stations-Simulation konsolidieren

### Aufgaben
- Hüllengeometrie in `geometry/hull.py` migrieren.
- `StationSimulation`-Klasse in `simulation.py` überführen.
- CLI-Starter (`blender_hull_simulation`, `blender_station_simulator`) vereinheitlichen.
- Automatisierte Tests für Hull-/Stationslogik schreiben.

### Aufgabenübersicht

| Aufgabe                                  | Zielordner/Modul                         | Fälligkeit     |
|------------------------------------------|------------------------------------------|----------------|
| Hull-Funktion migrieren                  | `geometry/hull.py`                       | 03.09.2025     |
| StationSimulation integrieren            | `simulation.py`                          | 06.09.2025     |
| CLI-Starter anpassen                     | `blender_hull_simulation/`, `blender_station_simulator/` | 10.09.2025     |
| Hull-/Stations-Tests                     | `simulations/tests`                      | 12.09.2025     |

---

## Sprint 4 (15.09.2025 – 26.09.2025): Dokumentation und Packaging

### Aufgaben
- README zweisprachig (DE/EN) erstellen.
- `pyproject.toml` bzw. `setup.py` schreiben, CI optional hinzufügen.
- Veraltete Skripte entfernen oder durch Importe ersetzen.

### Aufgabenübersicht

| Aufgabe                        | Zielordner/Modul             | Fälligkeit     |
|--------------------------------|------------------------------|----------------|
| README/Docs erstellen          | `simulations/`               | 18.09.2025     |
| Paketdateien anlegen          | Projekt-Wurzel               | 22.09.2025     |
| CI-Workflow (optional)         | `.github/workflows/`         | 24.09.2025     |
| Aufräumen alter Skripte        | Starter-Verzeichnisse        | 26.09.2025     |

---

## Hinweise

- **Bibliotheksprinzip**: Starter enthalten keine Berechnungslogik mehr.
- **Testpflicht**: Jede Funktion ist mit Unit-Tests abzusichern.
- **Zweisprachigkeit**: Dokumentation auf Deutsch & Englisch. Modulnamen englisch.

---

## GitHub-Verweise

- [`deck_calculator.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/sphere_space_station_simulations/deck_calculator.py)
- [`starter.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/deck_calculator/starter.py)
- [`adapter.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/deck_calculator/adapter.py)
- [`generate_3d_construction_csv.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/blender_deck_simulator/generate_3d_construction_csv.py)
- [`station_simulation.py`](https://github.com/robert2100-08-16/Sphere-Space-Station-Earth-ONE-and-Beyond/blob/main/simulations/deck_calculator/station_simulation.py)

