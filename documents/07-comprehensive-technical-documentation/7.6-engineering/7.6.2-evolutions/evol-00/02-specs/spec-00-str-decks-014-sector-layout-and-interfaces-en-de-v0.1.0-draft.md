---
id: spec-00-str-decks-014-0001
title: DECK 014 sector layout and interfaces
version: 0.1.0
state: draft
evolution: EVOL-00
discipline: STR
system: DECKS
system_id: "014"
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

# SPEC-00-STR-DECKS-014-sector-layout-and-interfaces-EN-DE-v0.1.0-DRAFT

**Project:** Sphere Space Station – Earth ONE (Ø 127.00 m)  
**Evolution:** EVOL-00 • **Spin Law:** 1 g at r = 38.00 m → ω = 0.50801 s⁻¹ ≈ 4.851 rpm  
**Document Status:** DRAFT v0.1.0 • **Date:** 2025-08-16

---

## 0. Summary / Kurzfassung (EN/DE)

**EN:** DECK 014 hosts the **nuclear primary systems (SMR)** and **power conversion/distribution** close to the hull for minimal thermal path length, while keeping equipment loads lower than on DECK 015. Compartmentalization, radial relief to space (VENT/BOP), and remote operations minimize operational risk and crew exposure.

**DE:** DECK 014 beherbergt die **nuklearen Primärsysteme (SMR)** sowie **Energie-Wandlung/Verteilung** in Hüllennähe für kurze Kühlwege – bei geringerer g-Belastung als auf DECK 015. **Kompartimentierung**, **radiale Entlastung ins All (VENT/BOP)** und **Remote-Operation** reduzieren Betriebsrisiken und Personalexposition.

---

## 1. Scope & Purpose / Zweck und Geltung

- **EN:** Sector-level layout, interfaces, safety zoning, and operations constraints for DECK 014.  
- **DE:** Sektor-Layout, Schnittstellen, Sicherheitszonen und Betriebsgrenzen für DECK 014.

**Dependencies / Abhängigkeiten:** Global Geometry & Gravitation SPEC (EVOL-00), DECK 013/015 specs, station-wide safety & ICD conventions.

---

## 2. Geometry & Environment / Geometrie & Umgebung

- **Radial band / Radialband:** **56.00–59.50 m** (Δr = 3.50 m)  
- **g-levels (ceiling→mid→floor):** **1.474 g → 1.520 g → 1.566 g**  
- **Deck height / Deckhöhe:** structural thickness per band; habitable clearance per compartment.  
- **Windows:** none / **Fenster:** keine (hull-near technical zone)

---

## 3. Sectorization & Access / Sektorierung & Zugänge

- **Sectors / Sektoren (12 × 30°):** A…L (A: 0–30°, B: 30–60° … L: 330–360°)  
- **Radial bulkheads / Radiale Schotts:** at all sector borders A|B,…,L|A; **PT-A** doors (primary), **PT-B** (service)  
- **Shafts / Schächte:** **HL-0/90/180/270** (heavy-lift), **PAX** at ±22.5°, 67.5° …, **UTIL** dual rings (inner/outer)  
- **Relief / Entlastung:** **VENT** to space via radial lines; **BOP** blow-out panels at designated sectors (no tangential relief)

---

## 4. Sector Allocation (Functional) / Sektor-Belegung (Funktional)

| Sector | HZ | EN – Primary Function | DE – Primärfunktion | Notes / Hinweise |
|:-----:|:--:|------------------------|---------------------|------------------|
| **A** | **3** | **SMR Cell-1 (Containment)**: RPV-1, primary loop-N, shield | **SMR-Zelle-1 (Containment)**: RDB-1, Primär-Loop-N, Schild | HL-0 access; VENT-014-A→Space + filtered; ESFAS/SIS |
| **B** | 2 | Nuclear auxiliaries (chem/boron, sampling) | Nuklear-Hilfssysteme (Chem/Bor, Probenahme) | Chem control, drains to 013 |
| **C** | 2 | **Power Conversion-N** (Brayton/Rankine skid) | **Energie-Wandlung-N** | Acoustic damping; THM tie-ins north |
| **D** | 2 | DC bus & switching (N) | DC-Bus & Schalter (N) | HL-90 access; DC-HV islanding |
| **E** | 1 | Remote shop & tele-ops | Werkstatt & Tele-Ops | Maintenance, robot staging |
| **F** | 1 | Inspection & AL-C airlocks | Inspektion & AL-C-Schleusen | Decon route to 013 |
| **G** | **3** | **SMR Cell-2 (Containment)**: RPV-2, primary loop-S, shield | **SMR-Zelle-2 (Containment)**: RDB-2, Primär-Loop-S, Schild | HL-180 access; VENT-014-G→Space + filtered |
| **H** | 2 | Nuclear auxiliaries (south) | Nuklear-Hilfssysteme (Süd) | Chem/boron systems |
| **I** | 2 | **Power Conversion-S** | **Energie-Wandlung-S** | THM tie-ins south |
| **J** | 2 | DC distribution (S/W) | DC-Verteilung (S/W) | HL-270 access |
| **K** | 1 | Water shield ring (upper) | Wasser-Schildring (oben) | Tie-in to 013/015 |
| **L** | 1 | Remote OPS & MCC (unmanned) | Fernbetrieb & Leitwarte (unbemannt) | Red/Blue fiber rings

**HZ classes:** 1 = normal technical, 2 = elevated energy/thermal, **3 = critical (nuclear/containment)**.

---

## 5. Interfaces / Schnittstellen

### 5.1 MECH (Structure & Mounts)
- Ring girder raster: **M18** on 014; isolation mounts ζ ≥ 0.08 at turbomachinery.
- Inspection clearances, crane/monorail in A/G cells.
- **DE:** Ringträger-Raster **M18**, Schwingungsdämpfung ζ ≥ 0,08; Kran/Monorail in A/G.

### 5.2 PWR (Electrical)
- **DC-HV backbone:** ±800 V split **DC-B1 (N/E)**, **DC-B2 (S/W)**; N+1 **UPS ≥ 30 min** for safety actuators.
- Islanding at **C/I** (conversion), switching at **D/J**.
- **DE:** DC-HV-Rückgrat wie oben; Inselnetze in C/I, Umschaltung D/J; USV N+1 ≥ 30 min.

### 5.3 THM (Thermal)
- **Primary loops** from **A/G** to **hull HX headers (N/S)** via shortest radial paths.
- Secondary headers to 015 (pump nodes D/J).
- **DE:** Primär-Loops A/G → Hüllen-Header (N/S); Sekundär-Header nach 015 (Pumpen D/J).

### 5.4 COM (Communications)
- Dual **Red/Blue fiber rings**; dedicated **SAFE-bus** for ESFAS/SIS; remote ops hub at **L**.
- **DE:** Doppelte Glasfaserringe; separater **SAFE-Bus**; Leitwarte in **L**.

### 5.5 GAS (Process & Inert)
- Inertization **N₂/Ar** feed from 015-H; monitored sector valves.
- **DE:** Inertisierung **N₂/Ar** aus 015-H; Sektor-Drosseln überwacht.

---

## 6. Safety, Schotts & Relief / Sicherheit, Schotts & Entlastung

- **PT-A** main sector doors (motor/manual, interlocked), **PT-B** service doors (fail-safe closed).
- **AL-C** airlocks with Δp/O₂/smoke/temp dual sensors.
- **VENT-014-A/G→Space** via filtered trains; **BOP** as last resort in A/G; no tangential relief lines.
- **DE:** PT-A/-B wie oben; AL-C mit Zweifach-Sensorik; VENT/BOP radial; keine tangentiale Entlastung.

---

## 7. Operations & Human Factors / Betrieb & HF

- **Exposure:** Category **E** in A/G (≤ 2 h), **D** elsewhere (≤ 4 h); **remote ops default**.
- **Wayfinding:** sector color codes; restricted access badges.
- **DE:** Verweilen: **E** in A/G (≤ 2 h), sonst **D** (≤ 4 h); **Remote-Betrieb** Standard.

---

## 8. Verification & Acceptance / Verifikation & Abnahme

- **Containment tests:** proof/leak-down A/G; interlock & ESFAS functional.
- **Thermal:** flow/ΔT capacity to hull HX; pump N+1 failover.
- **Electrical:** islanding switchover; UPS autonomy ≥ 30 min.
- **DE:** Dichtigkeits-/Funktionstests gemäß obigen Punkten.

---

## 9. ICD & Naming / Bezeichner

- **Shafts:** `HL-0|90|180|270`, `PAX-22.5|…|337.5`  
- **Relief:** `VENT-014-<Sector>`, `BOP-014-<Sector>`  
- **Nuclear cells:** `SMR-014-A|G`, Conversion: `PCON-014-C|I`

---

## 10. Change Log / Änderungshistorie

- v0.1.0 (2025-08-16): Initial EVOL-00 layout, interfaces, safety & OPS limits.

