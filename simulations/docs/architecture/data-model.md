# 1. Datenmodell

Dieses Dokument beschreibt die Dataclasses, die das interne Stationsmodell repräsentieren.

- **Deck**: Zylindrisches Deck mit Innen-/Außenradius, Höhe sowie abgeleiteten Werten wie Netto-Radien, Basisfläche und Volumen. Fenstergruppen können hinterlegt werden. Optional werden Stützen pro Deck berechnet.
- **Hull**: Kugelförmige Hülle mit Fenstern und berechneter Oberfläche sowie Volumen. Docking-Ports können entlang des Äquators platziert werden.
- **Wormhole**: Zentrales Zylindertunnel mit Radius, Höhe und optionaler Baseringstärke.
- **StationModel**: Aggregiert Decks, Hülle und optional das Wurmloch.

Die Implementierung befindet sich in [`simulations/sphere_space_station_simulations/data_model.py`](../../sphere_space_station_simulations/data_model.py).
