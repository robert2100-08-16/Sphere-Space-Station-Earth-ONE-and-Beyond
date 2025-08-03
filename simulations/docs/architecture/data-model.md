# 1. Datenmodell

Dieses Dokument beschreibt die Dataclasses, die das interne Stationsmodell repräsentieren.

- **Deck**: Einzelnes Deck mit Innen- und Außenradius sowie Höhe.
- **Hull**: Umhüllt die Decks und definiert die Hüllengeometrie.
- **StationModel**: Aggregiert alle Decks und globale Parameter.

Die Implementierung befindet sich in [`simulations/sphere_space_station_simulations/data_model.py`](../../sphere_space_station_simulations/data_model.py).
