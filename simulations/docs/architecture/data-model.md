# 1. Datenmodell

Dieses Dokument beschreibt die Dataclasses, die das interne Stationsmodell repräsentieren.

- **Deck**: Zylindrisches Deck mit Innen-/Außenradius, Höhe sowie abgeleiteten Werten wie Netto-Radien, Basisfläche und Volumen. Fenstergruppen können hinterlegt werden.
- **Hull**: Kugelförmige Hülle mit Fenstern und berechneter Oberfläche sowie Volumen.
- **Wormhole**: Zentrales Zylindertunnel mit Radius, Höhe und optionaler Baseringstärke.
- **StationModel**: Aggregiert Decks, Hülle und optional das Wurmloch.

Die Implementierung befindet sich in [`simulations/sphere_space_station_simulations/data_model.py`](../../sphere_space_station_simulations/data_model.py).
