---
id: "EVOL-00-baseline-freeze"
title: "EVOL-00 — Earth ONE (Ø 127 m): Baseline v1.0 — Kurzblatt"
version: v1.0.0
state: BASELINED
evolution: EVOL-00
discipline: SYSTEM
owner: "CTO Office (J. Frame) · Chief Engineer (Theo)"
reviewers: ["SGI Lina","Mara Flux","Elias Core"]
date: 2025-08-25
lang: DE
---

# EVOL-00 — Earth ONE (Ø 127 m) · Baseline v1.0 — Kurzblatt

**Zweck:** Minimal **vollständiger** Demonstrator (LEO). Architektur, Sicherheit, Build–Test–Operate.  
**Crew / Residents:** ~700 Personen (Mischung aus Crew, Wissenschaft, Familien).  
**Masse (dry+ops window):** ~310.000–320.000 t.  
**Drehung / Spin-Law:** 1 g @ r ≈ 38 m → ~4,851 rpm (Baseline).  
**Gravitationszonen:** Mikro-g im Achskanal (DECK 000), sanfter Gradient zu ~1 g in Wohn- und Arbeitszonen.

## Struktur & Geometrie (Kurz)
- **Hauptkörper:** Kugel Ø 127 m; integriertes Coaxial-Zylindersystem („Deck-Zylinder“).  
- **Decks:** DECK 000 (Achskanal „Wormhole“), danach ab **DECK 001** in 3,5-m-Bruttohöhen rasternd.  
  - **DECK 000:** Radius 0,0 m bis **10,5 m** Zylinder-ID (inkl. Wand).  
  - **DECK 001:** Radius **10,5 m** bis **14,0 m** (inkl. Wand).  
  - **DECK n:** Radius Start = 10,5 m + (n−1)×3,5 m; Radius Ende = Start + 3,5 m.
- **Primärgitter:** Meridionale und Breiten-Rippen (SiC/SiC-dominant), ringförmige Druckschotten, Crash-Bulkheads.

## Andocken & „Wormhole“
- **Polar-Ports:** Nord/Süd-Dock (extern) mit redundanten Equalize-Pfade.  
- **Achskanal (Wormhole):** Mikro-g Korridor; Service-Tubes; Not-Shelter.  
- **Throats (EVOL-00):** 20 m Durchmesser.

## Lebenserhaltung & Energie (Baseline)
- **Energie:** SMR-Fission (primär), Solar-Arrays (sekundär), chemische Not-Reserven.  
- **LSS:** Geschlossene Kreisläufe (H₂O, O₂/CO₂, Nährstoffe) mit „storm shelter“-Zonen.  
- **Brandschutz:** Sektorierte O₂-Management-Zonen; Inertion-Optionen; Hot-Work-Permits.

## Sicherheit (Top-Linien)
- **HAZ-Katalog:** SPEC-00-HAZARD v0.1 (IDs, Schwere, Gegenmaßnahme).  
- **VENT/BOP:** Ringförmige Vent-/Blow-Off-Panels, druckgestufte Equalize-Sequenzen.  
- **POL-GUARD:** Zugang/Prozedere (light) eingeführt; Crew-Drills quartalsweise.

## Verifikation & Exit-Kriterien
- **V&V:** Struktur/Spin/Deck-000 nachgewiesen; HZ-Matrizen freigegeben; SSOT eingeführt.  
- **Ops-Nachweis:** 180 Tage bei ≥ 75 % Belegung; Safety-KPI innerhalb Budget; Mean-Time-to-Equalize belegt.

> **Freeze-Umfang v1.0:** Geometrie, Spin-Parameter, Dock-Topologie (EVOL-00), LSS-Baseline, Safety-Schichten, HAZ-Index-Verlinkung.
