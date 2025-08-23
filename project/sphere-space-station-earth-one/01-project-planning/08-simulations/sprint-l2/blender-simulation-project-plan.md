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
source_of_truth: true
supersedes: null
superseded_by: null
rfc_links: []
adr_links: []
cr_links: []
date: 1970-01-01
lang: EN
---

Blender‑Simulation der Sphere‑Station
Dieses Verzeichnis enthält eine Beispiel‑Blender‑Simulation für die Sphere Space Station „Earth ONE“. Ziel ist es, auf Grundlage der vorhandenen Deck‑Berechnungen eine dreidimensionale Darstellung des Stationsinneren zu erzeugen und dabei alle relevanten Maße und Ausstattungsmerkmale aus dem Projekt zu berücksichtigen.
Struktur
simulations/blender_simulation/
├── blender_deck_simulation.py          # Blender‑Skript zum Erzeugen der Deck‑Modelle
├── deck_3d_construction_data.csv       # aus Deck‑Berechnung abgeleitete Daten für die 3D‑Konstruktion
└── README.md                           # diese Anleitung
deck_3d_construction_data.csv
Die CSV‑Datei enthält pro Deck sämtliche für die 3D‑Konstruktion notwendigen Geometriedaten und einige Ausstattungsmerkmale:
    • Deck – Name des Decks (z. B. „Deck 004“)
    • Inner/Outer Radius (m) – innerer bzw. äußerer Radius des Decks in Metern
    • Deck Height (m) – Gesamthöhe des Decks (inkl. Deckenstärke)
    • radial_thickness_m – Differenz zwischen äußerem und innerem Radius (Materialstärke)
    • windows_count – geschätzte Anzahl der Fenster entlang des Deckumfangs (Berechnung basiert auf einem Verhältnis von 20 % Fensterfläche und einer angenommenen Fensterbreite von 2 m)
    • window_material, window_total_thickness_cm, structure_material – aus den technischen Dokumenten abgeleitete Materialvorschläge
    • usage – vorgesehene Nutzung des Decks (Docking, Wohnen, Industrie, Lager …)
    • Rotation Velocity, Centrifugal Acceleration – aus der Deck‑Berechnung übernommen und können später zur Materialauslegung oder für Animationen genutzt werden
Diese Datei kann bei Bedarf ergänzt oder geändert werden, um weitere Merkmale abzubilden (z. B. Einbauten, Kabinen, Aufzugsschächte usw.).
blender_deck_simulation.py
Das Python‑Skript wird mit der integrierten Blender‑API (bpy) ausgeführt und erzeugt aus der CSV‑Datei eine einfache 3D‑Repräsentation:
    1. Bereinigung der Szene – Entfernt alle vorhandenen Objekte aus der aktiven Szene.
    2. Erzeugung der Decks – Für jedes Deck wird ein hohles Zylindersegment erstellt. Die innere und äußere Zylinderhülle werden per Boolean‑Modifikator zu einem Ring („Donut“) verbunden. Die Decks werden der Reihe nach entlang der Z‑Achse gestapelt.
    3. Wurmloch/Zentralzylinder – Ein durchgehender Zylinder mit dem Radius des innersten Decks modelliert den zentralen Durchgang („Wurmloch“).
    4. Sockelringe – Am oberen und unteren Ende des Wurmlochs werden zwei Sockelringe angelegt, deren Radius 20 % größer ist als der Wurmlochradius.
    5. Sammlung – Alle erzeugten Objekte werden in einer Collection SphereDeckCollection gruppiert, damit die Szene übersichtlicher bleibt.
Die erzeugten Geometrien dienen als Ausgangspunkt. Materialien, Texturen, Fensteröffnungen und weitere Ausstattung können anschließend manuell in Blender hinzugefügt oder durch weitere Skripte ergänzt werden.
Ausführen der Simulation
    1. Blender installieren: Stellen Sie sicher, dass Blender ab Version 2.9 installiert ist.
    2. Projekt öffnen: Starten Sie Blender und öffnen Sie das Scripting‑Fenster.
    3. Skript ausführen: Laden Sie blender_deck_simulation.py im Text‑Editor, passen Sie bei Bedarf den Pfad zur CSV an und führen Sie das Skript mit Alt+P aus.
    4. Ergebnisse betrachten: Nach dem Ausführen befindet sich unter „Collection“ eine neue Gruppe namens SphereDeckCollection mit allen erzeugten Objekten. Nutzen Sie Blenders Werkzeuge, um sich durch die entstehende 3D‑Struktur zu bewegen.
Optional kann das Skript auch direkt über die Kommandozeile gestartet werden:
blender --python simulations/blender_simulation/blender_deck_simulation.py --background
In diesem Fall wird Blender im Hintergrund ausgeführt. Anschließend können Sie die generierte .blend‑Datei speichern und weiterverarbeiten.
Weiterentwicklung
    • Fenster und Einbauten: Die CSV enthält bereits die Spalte windows_count. Ein erweitertes Skript könnte diese Werte nutzen, um pro Deck Fensteröffnungen entlang des Umfangs zu bohren oder separate Objekte für Fenster einzufügen.
    • Dynamische Animation: Die in der Deck‑Berechnung angegebenen Rotationsgeschwindigkeiten und Zentrifugalbeschleunigungen können zur Animation der Station verwendet werden (z. B. Rotieren um die Z‑Achse).
    • Materialzuweisung: Basierend auf den Materialspalten lässt sich jedes Deck oder Bauteil mit spezifischen Shadern versehen.
Diese Simulation stellt nur einen ersten Schritt dar. Für eine detailgetreue, fotorealistische Darstellung müssen weitere Daten (u. a. Kabinenlayouts, Einrichtungsgegenstände, Beleuchtungsszenarien) integriert werden.
