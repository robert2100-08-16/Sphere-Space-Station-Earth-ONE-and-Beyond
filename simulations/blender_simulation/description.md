# Beschreibung der Deckdaten

Diese Datei erläutert die Struktur der CSV `deck_3d_construction_data.csv`. Die Werte stammen aus den Berechnungen des Skriptes `generate_3d_construction_csv.py` und dienen der Erstellung der 3D-Segmente in Blender.

## Spaltenübersicht

- **Deck** – Kennung des Decks (`Deck 000` bis `Deck 015`).
- **usage** – vorgesehene Nutzung (z. B. "Residential/Operational").
- **Inner Radius (m)** – Radius bis zur inneren Deckwand.
- **Outer Radius (m)** – Radius bis zur äußeren Deckwand.
- **Outer Radius netto (m)** – nutzbarer Außenradius abzüglich Hüllenmaterial.
- **radial_thickness_m** – Differenz aus äußerem und innerem Radius (Wandstärke).
- **Deck Height (m)** – Bruttohöhe des Decks inklusive Boden und Decke.
- **Deck Height netto (m)** – nutzbare Innenhöhe.
- **windows_count** – Anzahl der eingeplanten Fenster.
- **window_material** – Aufbau des transparenten Materials.
- **window_total_thickness_cm** – Gesamtdicke des Fensterpakets in Zentimetern.
- **structure_material** – vorgesehenes Konstruktionsmaterial der Deckstruktur.
- **Rotation Velocity @ radius netto (m/s)** – Umfangsgeschwindigkeit am nutzbaren Außenradius bei gegebener Winkelgeschwindigkeit.
- **Centrifugal Acceleration @ radius netto (m/s²)** – resultierende Zentrifugalbeschleunigung am nutzbaren Außenradius.

## Hintergrund

Die Daten bilden die Grundlage für die Konstruktion der Sphere-Station in der Blender-Simulation. Aus dem Innen- und Außenradius ergeben sich die Abmessungen jedes Ringsegments. Die Brutto- und Nettohöhen geben Auskunft über den verfügbaren Raum, während die berechnete Umfangsgeschwindigkeit und Beschleunigung die simulierte Gravitation bestimmen. Die Fensteranzahl orientiert sich an der Ringgröße (ca. ein Fenster je 1,6 m Umfang).

