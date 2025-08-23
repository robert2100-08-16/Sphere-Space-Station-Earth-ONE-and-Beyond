---
id: spec-00-str-decks-deck001-0001
title: DECK001 transfer node and radial systems
version: 0.1.0
state: draft
evolution: EVOL-00
discipline: STR
system: DECKS
system_id: "DECK001"
seq: "0001"
owner: "@sgi-lina"
reviewers:
  - "@eng-elias"
  - "@eng-leo"
source_of_truth: true
supersedes: []
superseded_by: []
rfc_links: []
adr_links: []
cr_links: []
date: 2025-08-16
lang: en-de
---

# SPEC-00-STR-DECKS-DECK001-0001-transfer-node-and-radial-systems-EN-DE-v0.1.0-DRAFT

**The Engineering of DECK001 – Reception, Transfer & Radial Systems**  
**Document status:** Draft (EVOL-00 baseline)  
**Date:** 2025-08-16  
**Applies to:** Earth ONE class sphere station (Ø 127 m)

---

## 1. Abstract / Zusammenfassung (EN/DE)

**EN:** DECK 001 is the first pressurized distribution ring outside the axial DECK000 (“Wormhole”) and acts as the main reception level for incoming crew and cargo. It integrates radial pressure/fire bulkheads, radial transport (heavy-lift & passenger elevators, service tunnels), tangential and polar corridors, and reception/transfer airlocks linking the docking rings in DECK000 to DECK001 and onward to the outer decks. Geometrically it spans **rᵢ = 10.5 m** to **rₒ,net = 13.5 m** with **deck height = 3.0 m**; nominal centrifugal acceleration at the net radius is **3.38 m/s² (~0.34 g)**.

**DE:** DECK 001 ist der **erste druckbeaufschlagte Verteilring** außerhalb des axialen DECK 000 („Wormhole“) und bildet die **Haupt-Empfangsebene** für ankommende Personen und Fracht. Er integriert **radiale Druck-/Brandschotts**, **Radialtransport** (Heavy-Lift- & Personenaufzüge, Servicetunnel), **tangentiale und polwärts gerichtete Bahnen & Wege** sowie **Empfangs- und Transfer-Airlocks** von den Docking-Ringen in DECK 000 zu DECK 001 und weiter zu den Außen-Decks. Geometrisch liegt DECK 001 zwischen **rᵢ = 10.5 m** und **rₒ,net = 13.5 m** bei **Deckhöhe = 3.0 m**; die nominelle Zentrifugalbeschleunigung am Nettradius beträgt **3.38 m/s² (\~0.34 g)**.

---

## 2. Baseline Geometry & Environment (EVOL-00)

* **Radial band:** inner radius **10.5 m**, net outer radius **13.5 m**, height **3.0 m**.  
  **Tangential length:** ~**124.24 m** (inner) to **123.07 m** (outer).
* **Gravity:** ~**3.38 m/s²** at net radius (EVOL-00 spin law).
* **Deck role:** Mid-gravity deck for **residential/operational** uses; serves as **primary reception & distribution hub** from the axial wormhole to outer decks.

---

## 3. Functions & Scope

1. **Reception & Transfer / Empfang & Verteilung**
   - **EN:** Secure intake and distribution of crew, passengers, and cargo from DECK000 (docking rings) into the ring topology, including quarantine and safety checks.
   - **DE:** Sichere Aufnahme/Verteilung von Crew, Passagieren und Fracht aus DECK 000 (Docking-Ringe) in die Ring-Topologie, inkl. Quarantäne- und Sicherheits-Checks.
2. **Radial Core Access / Radialer Kernzugang**
   - **EN:** Heavy-lift and passenger elevators plus service tunnels connect **all decks** from the core to the outer bands.
   - **DE:** Aufzüge (Heavy-Lift & Personen) und Servicetunnel verbinden **alle Decks** vom Core zu den Außenlagen.
3. **Tangential & Polar Mobility / Tangentiale & polare Mobilität**
   - **EN:** Circumferential paths and polar (meridional) spurs route traffic to near-pole nodes (interfaces to DECK000).
   - **DE:** Umlaufende Wege/Bahnen + polwärts gerichtete (meridionale) Zubringer zu den polnahen Knoten (Schnittstellen zu DECK 000).
4. **Safety Envelope / Sicherheitsrahmen**
   - **EN:** Segmented pressure/fire bulkheads, pressure doors, airlocks, and inert-gas fire suppression.
   - **DE:** Segmentierte **Druck-/Brandschott-Geometrie**, Drucktüren, Airlocks, inert-Gas-Brandunterdrückung.

---

## 4. System Elements (Baseline Design)

### A) Radiale Druck- & Brandschotts (Compartmentation)

* **Sektorierung:** 12 keilförmige Sektoren (alle 30°) durch **radiale Schotts** von **r = 10.5 m → 13.5 m**; bildet eigenständige **Druck- & Brandschutz-Kompartimente**.
* **Ausführung:** Mehrlagen-Composit-Schottplatten (SiC-Verbund) mit metallischen Rahmen; integrierte **Drucktüren (A0/A60-äquivalent, Raumfahrtstandard)** auf jedem Sektor-Tangentenweg.
* **Funktion:** **Schnellisolierung** bei Dekompression/Feuer; **automatisches Schließen** via Brand-/Drucksensorik, freigabepflichtige Notentriegelung.
* **Brandunterdrückung:** **Inertgas (Argon/N₂)** sektoral; Trigger bei Flammen-/Rauchdetektion und Temperaturanstieg.

### B) Radialer Transport – Heavy-Lift & Passenger Elevators

* **Mandat:** durchgehende Verbindung **DECK 000 ⇄ 015** (Personen & Fracht); redundante Pfade.
* **Layout (EVOL-00):**
  * **4 Heavy-Lift-Schächte** (90°-Versatz), freie Lichtfläche ≥ 4.0 m × 3.0 m, **50 kN Nutzlast**, Dock-/Paletten-Kompatibilität.
  * **8 Personenaufzüge** (alle 45°, um 22.5° gegenüber Heavy-Lift versetzt), Kabinen 1.6 m × 1.6 m, 10–12 Pax.
  * **Stationsnorm-Interface** (mechanisch/elektrisch/Datentechnik) identisch über alle Decks; **Not-Handläufe** & **Leiterläufe** im Schacht.
* **Sicherheit:** **Druckschotte** auf jedem Deck-Durchtritt, **Doppeltüren** als Schleusen (Interlock), unabhängige **DC-Bus-USV** für Tür-/Bremssysteme.

### C) Radiale Servicetunnel (Utilities Spine, beginnend auf DECK 001)

* **Zweck:** Trassen für **Luft/CO₂-Rücklauf, Wasser/Kondensat, Energie-DC-Busse, Daten/Comms**, Wärme-Sekundärkreise.
* **Querschnitt:** typ. ≥ 1.2 m Gangbreite; **doppelte Trunkings** (getrennte rote/gelbe Utility-Seite) für Instandhaltung im laufenden Betrieb.
* **Druck-/Brand-Zonen:** **Abschluss-Türen** pro Sektor; **Schnell-Isolierungs-Klappen** in Lüftung.

### D) Tangentiale Bahnen & Wege (on-Deck Mobility)

* **Gehwege:** 2 × umlaufende **3.0 m Korridore** (inner/outer ring), Farbleitsystem & Photometrie gemäß Stationsstandard.
* **Fördertechnik:** **Conveyors/Schienenträger** für Material-Fluss, **kleine Rangier-Rail-Vehikel** in EVOL-00 (Handbetrieb/halbautonom).

### E) Polwärts gerichtete Zubringer (Meridional Spurs)

* **Definition:** kurze **meridionale Trassen** je Quadrant, die von DECK 001 **Richtung Pol** in **Wurmlöcher-Knoten** (Docking-Ring-Ebenen in DECK 000) führen.
* **Zweck:** schnelles **Crew-/Fracht-Umsetzen** zwischen Ring-Verkehr und axialem Docking-Korridor; Notausweichrouten.
* **Schnittstellen:** **air-tight Transfer-Hatches** zu **DECK 000 Docking-Rings 01–04** (EVOL-00 baseline), inklusive **Druck-Isolationspunkte** an Ring-Grenzen (Rings können als Kompartiment versiegelt werden).

### F) Empfangs- & Durchschleuseanlagen (DECK 000 → DECK 001 → Outer Decks)

* **Reception Vestibules (RV-Nodes):** vier **Empfangs-Knoten** (je Quadrant), direkt an die meridionalen Zubringer gekoppelt.
  * **Funktionen:** Einreise-/Sicherheits-Check, **medizinischer Quick-Screen**, **Baggage-Staging**, **Route-Guidance**.
  * **Schleusenlogik:** **Doppelschleusen** mit **autom. Druckangleich**, **Blast-Shutters** & **MMOD-Shades** nach Fenster-/Öffnungs-Norm.
* **Weiterleitung:** kurze Wege zu **Passenger-Lobbies** (Personenaufzüge) und **Cargo-Bays** (Heavy-Lift).
* **Notbetrieb:** **Safe-Hold-Bay** je RV-Node (Atemschutz, Comms, Notenergie).

### G) Drucktüren, Airlocks & Schutzsysteme

* **Türklassen:**
  * **PT-A (Pressure-Tight, primary):** Haupt-Drucktüren der Sektorschotts (manuell + motorisch, Interlock).
  * **PT-B:** Türen in Servicetunneln, Aufzugsvorlauf, Technikräumen.
  * **AL-C (Airlock):** Personen-/Fracht-Schleusen mit zweifach redundanter Sensorsuite (Δp, O₂, Rauch, Temp).
* **Brand & Inertgas:** Abteilungsweise **Argon/N₂-Flutung**; Erkennung über **Rauch/Temp**-Arrays; **Hand-Pulls** an allen Korridor-Schnittstellen.

### H) Polar Outer Hull (Deck 001 Band)

* **Außenhülle (polnah, Deck-001-Band):** **~0.5 m** dicke mehrlagige Composit-Hülle als Basis-Thermal-/Strahlungsschutz mit Anbindung an polare Struktur-Ringe; lokale **Durchdringungen** (Meridional-Spurs, Sensorik) mit metallischen C-Seals.
* **Materialsysteme:** SiC-Verbund, Polyimid-/Siloxan-Elastomere, Silica-Aerogel-Isolationslagen; Auswahl nach **LEO-Fenster/Glazing-Spec** für optische Öffnungen.

---

## 5. Interfaces

* **To DECK 000 (Wormhole):** Anschluss an **Docking-Ring-Ebenen** via **meridionale Zubringer** + **Reception Vestibules**; **Druck-Isolationspunkte** an Ring-Grenzen (ring-as-compartment).
* **To Outer Decks (002…):** **Radial-Aufzüge** (Heavy-Lift & Personen) + **Servicetunnel** setzen Vertikal-Kontinuität; Norm-Interface für Mechanik/Power/Comms identisch über alle Decks.
* **To Station Systems:** Luft/CO₂-Rücklauf, Wasser/Kondensat, **Dual-DC-Bus** + lokale **UPS** für safety-kritische Aktoren, Comms-Rail.

---

## 6. Operations & Human Factors

* **Wayfinding:** Farbcodierte Sektor-/Spur-Leitsysteme, polwärts = blau, radial = gelb, tangential = grün; Piktogramme gemäß Stationsstandard.
* **Flow-Separation:** **Crew/Service** vs. **Passenger/Fracht** getrennt; Querverbindungen über Schleusen-Türen.
* **Ergonomie:** Handläufe durchgehend; Beleuchtung mit Nominal-/Notlicht-Profilen.

---

## 7. Materials & Compliance

* **Primär:** **SiC-Verbund** (Struktur), **Inconel/Stahl** in Rahmen/Verstärkungen; **Elastomere** & **C-Seals** an Druckschnittstellen.
* **Glazing/Shutters:** gemäß **LEO Window Specification** (ALON/Saphir, Fused Silica, Polycarbonat, Borosilicat; Blast-Shutters & MMOD-Shades).
* **Safety Protocols:** **Inertgas-Löschung**, Hüllen-/Strahlungsschutz, MMOD-Resistenz, Biohazard-Filtration – station-weit gültig.

---

## 8. Verification & Acceptance (V&V)

* **Drucktests:** sektorweise Proof- & Leak-Tests (AL-C Schleusen, PT-A/-B Türen).
* **Brand-Szenarien:** Inertgas-Auslösung, Evakuierungs-Drills, Tür-Interlock-Failover.
* **Transport:** Last-/Funktionstests Aufzüge (50 kN), Not-Bremse/USV-Autonomie ≥ 30 min.

---

## 9. Open Parameters (TBD/TBC)

* Exakte **Anzahl & Position** der Heavy-Lift/Passenger-Schächte (Feinabgleich mit Nutzungskarte DECK 001).
* **Meridionale Spur-Routing** zu spezifischen Docking-Ringen (abhängig von Traffic-Modell DECK 000).
* **Brandschutz-Klassifizierung** der Türsysteme vs. Raumnutzung (A0/A60-Mapping).
* **Thermalloop-Führung** & Radiator-Tie-Ins im polnahen Bereich.

---

## 10. Drawing & Data References

* **Deck geometry & dynamics:** DECK 001 radii/height, net g-level, tangential lengths.
* **Access systems (elevators, tangential walkways):** baseline requirements.
* **Wormhole interface & ring compartmentalization:** docking rings, isolation at ring boundaries.
* **Safety & materials:** inert-gas protocols, hull thickness, materials & window spec.

---
