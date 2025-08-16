---
id: spec-00-str-decks-013-0001
title: DECK 013 sector layout and interfaces
version: 0.1.0
state: draft
evolution: EVOL-00
discipline: STR
system: DECKS
system_id: "013"
seq: "0001"
owner: "@sgi-lina"
reviewers:
  - "@eng-elias"
  - "@eng-leo"
source_of_truth: false
supersedes: []
superseded_by: []
rfc_links: []
adr_links: []
cr_links: []
date: 2025-08-16
lang: en-de
---
# SPEC-00-STR-DECKS-013-sector-layout-and-interfaces-EN-DE-v0.1.0

**Project:** Sphere Space Station – Earth ONE (Ø 127.00 m)  
**Evolution:** EVOL-00 • **Spin Law:** 1 g at r = 38.00 m → ω = 0.50801 s⁻¹ ≈ 4.851 rpm  
**Document Status:** DRAFT v0.1.0 • **Date:** 2025-08-16

---

## 0. Summary / Kurzfassung (EN/DE)

**EN:** DECK 013 serves as a **buffer & service ring** between nuclear/thermal systems (014/015) and the habitable mid-decks. It hosts **water/poly shielding**, **heat-exchanger galleries**, **service corridors** and **decon/airlock nodes**. Low-risk technical zones (HZ-1) dominate; select HZ-2 areas in heat-exchanger galleries.

**DE:** DECK 013 fungiert als **Puffer- & Service-Ring** zwischen den Nuklear-/Thermik-Decks (014/015) und den mittleren Habitatzonen. Es beherbergt **Wasser/Poly-Schilde**, **Wärmetauscher-Galerien**, **Servicegänge** sowie **Dekon-/Schleusenknoten**. Überwiegend **HZ-1** (geringes Risiko), punktuell **HZ-2** in den Wärmetauscher-Galerien.

---

## 1. Scope & Purpose / Zweck und Geltung

- **EN:** Sector-level layout, interfaces, safety zoning, and OPS constraints for DECK 013.  
- **DE:** Sektor-Layout, Schnittstellen, Sicherheitszonen und Betriebsgrenzen für DECK 013.

**Dependencies / Abhängigkeiten:** Global Geometry & Gravitation SPEC (EVOL-00), DECK 014/015 specs, station-wide safety & ICD conventions.

---

## 2. Geometry & Environment / Geometrie & Umgebung

- **Radial band / Radialband:** **52.50–56.00 m** (Δr = 3.50 m)  
- **g-levels (ceiling→mid→floor):** **1.382 g → 1.428 g → 1.474 g**  
- **Deck height / Deckhöhe:** structural thickness per band; habitable clearance per compartment.  
- **Windows / Fenster:** none / keine (technischer Pufferbereich)

---

## 3. Sectorization & Access / Sektorierung & Zugänge

- **Sectors / Sektoren (12 × 30°):** A…L (A: 0–30°, …, L: 330–360°)  
- **Radial bulkheads / Radiale Schotts:** at all sector borders A|B,…,L|A; **PT-A** doors (primary), **PT-B** (service)  
- **Shafts / Schächte:** **HL-0/90/180/270** (heavy-lift), **PAX** at ±22.5°, 67.5° …, **UTIL** dual service trunks (inner/outer)  
- **Relief / Entlastung:** **VENT** to space via radial lines; **no BOP** foreseen for 013 (low-energy fluids)

---

## 4. Sector Allocation (Functional) / Sektor-Belegung (Funktional)

| Sector | HZ | EN – Primary Function | DE – Primärfunktion | Notes / Hinweise |
|:-----:|:--:|------------------------|---------------------|------------------|
| **A** | 1 | Water/Poly shield (N arc) | Wasser/Poly-Schild (Nordbogen) | Tie-in to 014/015; level/sampling |
| **B** | 1 | Water/Poly shield (NNE) | Wasser/Poly-Schild (NNO) | Segment isolation valves |
| **C** | 1 | Water/Poly shield (NE) | Wasser/Poly-Schild (NO) | Leak sumps, monitors |
| **D** | 1 | Water/Poly shield (ENE) | Wasser/Poly-Schild (ONO) | **HL-90** nearby |
| **E** | 2 | HX gallery (N/E headers) | HX-Galerie (Nord/Ost) | THM tie-ins to hull headers |
| **F** | 2 | HX gallery (E) | HX-Galerie (Ost) | Acoustic damping, access control |
| **G** | 1 | Water/Poly shield (S arc) | Wasser/Poly-Schild (Südbogen) | **HL-180** nearby |
| **H** | 1 | Water/Poly shield (SSW) | Wasser/Poly-Schild (SSW) | Segment isolation valves |
| **I** | 2 | HX gallery (S/W headers) | HX-Galerie (Süd/West) | THM tie-ins to hull headers |
| **J** | 2 | HX gallery (W) | HX-Galerie (West) | Access from **HL-270** |
| **K** | 1 | Service & decon node | Service & Dekon-Knoten | **AL-C** airlocks, workshop |
| **L** | 1 | Service, metrology & sampling | Service, Messtechnik & Probenahme | Maint-LAN, stores

**HZ classes:** **1 = normal technical**, **2 = elevated energy/thermal**.

---

## 5. Interfaces / Schnittstellen

### 5.1 MECH (Structure & Mounts)
- Ring girder raster: **M18** on 013; saddle supports for ring tanks; inspection walkways; spill containment at low points.  
- **DE:** Ringträger-Raster **M18**; Auflager für Ringtanks; Inspektionsstege; Auffangwannen an Tiefpunkten.

### 5.2 PWR (Electrical)
- **DC-HV backbone** continuation (DC-B1/B2 split); MCC panels near HX galleries (**E/F/I/J**).  
- **UPS ≥ 30 min** for valve/VENT actuation & monitoring.  
- **DE:** DC-Rückgrat fortgeführt; MCC in **E/F/I/J**; **USV ≥ 30 min** für Ventile/VENT/Monitoring.

### 5.3 THM (Thermal)
- HX strings in **E/F/I/J** feed **hull HX headers** (N/E/S/W) with shortest radial routing.  
- Shield-water circuits in **A–D** and **G–H** can **absorb transient heat** and provide **biological shielding**.  
- **DE:** HX-Stränge **E/F/I/J** zu Hüllen-Headern; Schild-Wasserringe **A–D**, **G–H** als Wärmepuffer & biologischer Schild.

### 5.4 COM (Communications)
- Dual **Red/Blue fiber rings**; **Maint-LAN** drops in **K/L**; SAFE-bus pass-through for monitoring.  
- **DE:** Doppelte Glasfaserringe; **Maint-LAN** in **K/L**; SAFE-Bus-Durchleitung.

### 5.5 GAS (Process & Inert)
- Inert **N₂/Ar** feed (from 015-H) to 013 sector manifolds; monitored sector valves.  
- **DE:** Inertgas **N₂/Ar** aus 015-H; sektorseitige Verteilbalken mit Überwachung.

---

## 6. Safety, Schotts & Relief / Sicherheit, Schotts & Entlastung

- **PT-A** main doors at sector boundaries (motor/manual, interlocked); **PT-B** for service corridors (fail-safe closed).  
- **AL-C** airlocks at **K** (decon node) and selected gallery entries.  
- **VENT**: radial ducts from HX galleries to space; shield-water areas vent to dedicated scrubbers (no BOP planned on 013).  
- **DE:** PT-A/-B wie oben; **AL-C** in **K** und ausgewählten Galerien; **VENT** radial; Schild-wasser → Scrubber; **kein BOP** auf 013 vorgesehen.

---

## 7. Operations & Human Factors / Betrieb & HF

- **Exposure:** Category **C/D** (≤ 8 h / ≤ 4 h) depending on task; HX galleries treated as **HZ-2** with stricter access control.  
- **Wayfinding:** sector color codes; service/decon signage; low-noise policy in shield zones.  
- **DE:** Verweilen **C/D** je nach Aufgabe; HX-Galerien als **HZ-2** mit Zugangskontrolle; klare Wegführung & Lärmleitwerte.

---

## 8. Verification & Acceptance / Verifikation & Abnahme

- **Shield-water** integrity (proof/leak), overflow tests, level alarms.  
- **HX capacity** checks (flow/ΔT), redundancy (N+1 pumps upstream on 015 D/J).  
- **VENT** functional tests; **AL-C** pressure equalization & sensor redundancy checks.  
- **DE:** Dichtheit & Alarmierung Schild-wasser; HX-Kapazität/Redundanz; VENT-Funktion; AL-C-Prüfungen.

---

## 9. ICD & Naming / Bezeichner

- **Shafts / Schächte:** `HL-0|90|180|270`, `PAX-22.5|…|337.5`  
- **Relief / Entlastung:** `VENT-013-<Sector>`  
- **Shield tanks / Schilde:** `SHLD-013-<Sector>-<Nr>`  
- **HX strings / HX-Stränge:** `HX-013-<Sector>-<StringID>`  
- **Airlocks / Schleusen:** `ALC-013-<Node>`

---

## 10. Change Log / Änderungshistorie

- v0.1.0 (2025-08-16): Initial EVOL-00 buffer/service layout, interfaces, safety & OPS limits.