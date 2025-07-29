# Beschreibung der Deckdaten

Diese Datei erläutert die Struktur der CSV `deck_3d_construction_data.csv`. Die Werte stammen aus den Berechnungen des Skriptes `generate_3d_construction_csv.py` und dienen der Erstellung der 3D-Segmente in Blender.

## Grundbeschreibung was ein DECK ist
Der Raum zwischen einer koaxialer Sphere Röhre n (mit Durchmesser d1) und der nächsten koaxialen Sphere Röhre n+1 (mit Durchmesser d2, wobei d2 > d1).

## DECK 000 - Wurmloch
Merke DECK 000 (Wurmloch, vgl. ein gerades zentrisch durchgängiges Wurmloch durch einen Apfel) hat nur Fenster, Schleusen und Docking Bays in seiner Röhrenwand und ist an beiden Enden offen zum Wetlraum und demgemäß nicht bepressured (freier Raum, keine Atmospähre). 

## Spaltenübersicht

- **Deck** – Kennung des Decks (`Deck 000` bis `Deck 015`).
- **usage** – vorgesehene Nutzung (z. B. "Residential/Operational").
- **Inner Radius (m)** – Deckbeginn Radius.
- **Outer Radius (m)** – Deckende Radius, inkl. Röhrenwand (vgl. ein Rohr).
- **Outer Radius netto (m)** – Deckende Radius ohne Röhrenwand (vgl. der Inhalt eines Rohrs).
- **radial_thickness_m** – Deckhöhe inkl. Röhrenwand (vgl. ein Rohr).
- **Deck Height (m)** – Bruttohöhe des Decks inklusive Röhrenwand (Deckdecke), identisch mit **radial_thickness_m** (Duplette).
- **Deck Height netto (m)** – nutzbare Deck Innenhöhe (vgl. Raumhöhe eines Zimmers, eines mehrstockigen Gebäudes).
- **windows_count** – Anzahl der eingeplanten Außenfenster am DECK.
- **window_material** – Aufbau des transparenten Materials.
- **window_total_thickness_cm** – Gesamtdicke des Fensterpakets in Zentimetern.
- **structure_material** – vorgesehenes Konstruktionsmaterial der Deckstruktur.
- **Rotation Velocity @ radius netto (m/s)** – Umfangsgeschwindigkeit am Boden der sich drehenden Röhre (also am Deckboden) bei gegebener Winkelgeschwindigkeit.
- **Centrifugal Acceleration @ radius netto (m/s²)** – resultierende Zentrifugalbeschleunigung am Boden der sich drehenden Röhre (also am Deckboden).

## Hintergrund

Die Daten bilden die Grundlage für die Konstruktion der Sphere-Station in der Blender-Simulation. Aus dem Innen- und Außenradius ergeben sich die Abmessungen jeder Röhre. Die Brutto- und Nettohöhen geben Auskunft über den verfügbaren Raum, während die berechnete Umfangsgeschwindigkeit und Beschleunigung die simulierte Gravitation bestimmen (am Deckboden). Die Fensteranzahl orientiert sich an der verfügbaren Wand an der Deckaußenhülle und der Deckfunktion, Fenster gibt es nur bis Deck 012, da die Spährenhülle an den Outerdecks (> DECK 012) immer größere Bereiche des Decks einnehmen (vgl. einer Dachschrägen in einer Dachgeschoßwohnung).

