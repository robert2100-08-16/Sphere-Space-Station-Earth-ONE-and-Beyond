# Beschreibung der Deckdaten

Diese Datei erläutert die Struktur der CSV `deck_3d_construction_data.csv`. Die Werte stammen aus den Berechnungen des Skriptes `generate_3d_construction_csv.py` und dienen der Erstellung der 3D-Segmente in Blender.

## Grundbeschreibung was ein DECK ist
Der Raum zwischen einer koaxialer Sphere Röhre n (mit Durchmesser d1) und der nächsten koaxialen Sphere Röhre n+1 (mit Durchmesser d2, wobei d2 > d1).

## DECK 000 - Wurmloch
Merke DECK 000 (Wurmloch, vgl. ein gerades zentrisch durchgängiges Wurmloch durch einen Apfel) hat nur Fenster, Schleusen und Docking Bays in seiner Röhrenwand und ist an beiden Enden offen zum Wetlraum und demgemäß nicht bepressured (freier Raum, keine Atmospähre). 

## Spaltenübersicht

- **Deck** – Kennung des Decks (`Deck 000` bis `Deck 015`).
- **deck_usage** – vorgesehene Nutzung (z. B. "Residential/Operational").
- **inner_radius_m** – Deckbeginn Radius.
- **outer_radius_m** – Deckende Radius, inkl. Röhrenwand (vgl. ein Rohr).
- **outer_radius_netto_m** – Deckende Radius ohne Röhrenwand (vgl. der Inhalt eines Rohrs).
- **deck_height_m** – Bruttohöhe des Decks inklusive Röhrenwand.
- **deck_inner_height_m** – nutzbare Deck Innenhöhe (vgl. Raumhöhe eines Zimmers, eines mehrstockigen Gebäudes).
- **num_windows** – Anzahl der eingeplanten Außenfenster am DECK.
- **window_material** – Aufbau des transparenten Materials.
- **window_thickness_cm** – Gesamtdicke des Fensterpakets in Zentimetern.
- **structure_material** – vorgesehenes Konstruktionsmaterial der Deckstruktur.
- **rotation_velocity_mps** – Umfangsgeschwindigkeit am Boden der sich drehenden Röhre (also am Deckboden) bei gegebener Winkelgeschwindigkeit.
- **centrifugal_acceleration_mps2** – resultierende Zentrifugalbeschleunigung am Boden der sich drehenden Röhre (also am Deckboden).

## Hintergrund

Die Daten bilden die Grundlage für die Konstruktion der Sphere-Station in der Blender-Simulation. Aus dem Innen- und Außenradius ergeben sich die Abmessungen jeder Röhre. Die Brutto- und Nettohöhen geben Auskunft über den verfügbaren Raum, während die berechnete Umfangsgeschwindigkeit und Beschleunigung die simulierte Gravitation bestimmen (am Deckboden). Die Fensteranzahl orientiert sich an der verfügbaren Wand an der Deckaußenhülle und der Deckfunktion, Fenster gibt es nur bis Deck 012, da die Spährenhülle an den Outerdecks (> DECK 012) immer größere Bereiche des Decks einnehmen (vgl. einer Dachschrägen in einer Dachgeschoßwohnung).

