---
id: spec-00-str-sys-axial-radial-trade-0001
title: Variant study longitude vs latitude bulkheads
version: 0.1.0
state: draft
evolution: EVOL-00
discipline: STR
system: SYS-AXIAL-RADIAL-TRADE
system_id: "0001"
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
# SPEC-00-STR-SYS-AXIAL-RADIAL-TRADE-0001 — Variantenuntersuchung Längs-/Breitengrad-Schotten *(EVOL-00, 127 m)*

## Summary / Kurzfassung (EN/DE)

**EN:** Compares three structural and safety layouts for the sphere: **A) Longitudinal sectors**, **B) Latitudinal diaphragms ("LAT")**, **C) Combination**. Evaluates structural dynamics, pressure/fire/hazard containment, operations & maintenance, routing complexity, mass/manufacturing, and expandability. Result: **Option C** offers the best performance; recommended as baseline (EVOL-00 with 12 sector bulkheads A–L plus 3 LAT discs S40/EQ/N40, expanding to 7 LAT in EVOL-01).

**DE:** Vergleich dreier Struktur- und Safety-Layouts für die Sphäre: **A) Längsgrade** (radiale Sektorschotten), **B) Breitengrade** (axiale Ring-Diaphragmen, „LAT“), **C) Kombination**. Bewertet werden **Statik/Dynamik**, **Druck/Brand/Hazard**, **OPS & Wartung**, **Routing/Komplexität**, **Masse & Fertigung**, **Erweiterbarkeit**. Ergebnis: Variante **C (Kombiniert)** liefert die beste Gesamtleistung; empfohlen als Baseline (EVOL-00 mit 12 Längsgrad-Schotten A–L + 3 LAT-Scheiben S40/EQ/N40, Ausbau zu 7 LAT in EVOL-01).

**Project:** Sphere Space Station — Earth ONE (Ø 127,00 m)
**Spin Law:** 1 g at r = 38,00 m → ω ≈ 0,508 s⁻¹ (≈ 4,85 rpm)
**Status:** DRAFT • **Date:** 2025-08-16

---

## Abstract / Kurzfassung

---

## 1 Scope & Assumptions / Geltung & Annahmen

* Sphäre Innenhülle: **Rₕ = 63,00 m**; Deckbänder **Δr = 3,50 m** von **r = 10,50…63,00 m** (DECK 001–015).
* **Druck-/Brand-Philosophie:** Radiale Entlastung (VENT/BOP) zur Hülle; tangentiale Entlastung vermeiden.
* **Design-Δp:** Voll-Δp-Szenario (1,0 atm) über **Sektor**; **LAT** als Diaphragmen nur mit **Equalize** (Design-Δp ≤ 0,2 atm).

---

## 2 Variantenbeschreibung

### A) Längsgrade (radiale Sektorschotten)

* 12 keilförmige Schotten A–L (alle 30°) über DECK 001–015; **PT-A/B** Türen und **AL-C** Schleusen an Durchtritten.
* Bilden mit Deck-Hoopringen einen **Mehrzellen-Torsionskasten** (Bredt-Batho).

### B) Breitengrade (axiale LAT-Diaphragmen)

* Ringförmige Diaphragmen senkrecht zur Drehachse; Innenloch (Core) \~ **12 m**; Ebenen z. B.: **S56, S40, S20, EQ, N20, N40, N56**.
* Funktion: **Schubscheiben**, axiale **Brand-/Hazard-Kappen**, akustische Barrieren; **keine Voll-Druckschotte**.

### C) Kombination (A + B)

* 12 Sektorschotten **+** 3–7 LAT-Scheiben; mechanisch als **Gitter-/Rippen-Schale** mit hoher **Torsions- & Biegesteifigkeit**, **axialer** und **radialer** Kompartmentierung.

---

## 3 Bewertungsmaßstäbe / Methods

* **Strukturell:** Torsionssteifigkeit (*J*) nach Bredt-Batho (Mehrzellen), axiale Diaphragma-Schubpfade, Ovalisationsbegrenzung.
* **Dynamik:** Anhebung Eigenfrequenzen (Barrel/Breathing), Dämpfung (Elastomerfugen), Dock/Triebwerksimpulse.
* **Safety:** Druck/Brand/Kryo/Nuklear-Eindämmung; VENT/BOP-Wirksamkeit; Rauch-/Gas-Migration.
* **OPS & Wartung:** Türen/Schleusen, Egress, Tele-Ops, Zugänglichkeit.
* **Routing/Komplexität:** MEP (THM/PWR/COM/GAS) Durchdringungen, Kollisionen.
* **Masse/Fertigung:** Fläche × t × ρ; Fertigungs-/Montagelogik; QC/Prüfbarkeit.
* **Erweiterbarkeit:** stufenweiser Ausbau, spätere Nachrüstung.

---

## 4 Variantenanalyse

### 4.1 Statik & Dynamik

| Kriterium               | A) Längsgrade         | B) Breitengrade            | C) Kombiniert                     |
| ----------------------- | --------------------- | -------------------------- | --------------------------------- |
| Torsion/J               | **Hoch** (Mehrzellen) | Mittel                     | **Sehr hoch** (Zellen + Scheiben) |
| Axiale Biegesteifigkeit | Mittel                | **Hoch** (Scheibenabstand) | **Sehr hoch**                     |
| Ovalisation/Öffnungen   | Gut                   | Gut                        | **Sehr gut**                      |
| Eigenfrequenzen         | ↑                     | ↑                          | **↑↑ (max)**                      |
| Akustik (Körperschall)  | Mittel                | **Gut**                    | **Sehr gut**                      |

**Begründung:** Längsgrade erzeugen geschlossene Zellen → **hohes J**. LAT kappen **axiale Dehnwege** → höhere **axiale** Steifigkeit. Kombination maximiert beides.

### 4.2 Safety (Druck/Brand/Hazard)

| Kriterium          | A            | B                         | C               |
| ------------------ | ------------ | ------------------------- | --------------- |
| Radiale Eindämmung | **Sehr gut** | Mittel                    | **Sehr gut**    |
| Axiale Eindämmung  | Mittel       | **Sehr gut**              | **Sehr gut**    |
| VENT/BOP-Führung   | Klar radial  | Klar radial               | **Klar radial** |
| Nuklear/Tank-Zonen | Gut          | **Sehr gut** (LAT-Kappen) | **Sehr gut**    |

**Begründung:** Radiale Schotten stoppen **seitliche** Ausbreitung; LAT deckeln **axiale** Heißgas-/Rauchpfade. Kombination liefert **2D-Kompartmentierung**.

### 4.3 OPS/Wartung & Routing

| Kriterium             | A               | B                       | C                              |
| --------------------- | --------------- | ----------------------- | ------------------------------ |
| Türen/Schleusenanzahl | **Geringer**    | Mittel                  | **Höher**                      |
| Wegführung/Egress     | Klar tangential | Zusätzliche Sperrebenen | **Sehr klar**, aber mehr Gates |
| MEP-Durchdringungen   | **Geringer**    | Mehr Portals/Equalizer  | **Höher**, aber definierter    |
| Integration/Upgrade   | Einfach         | Mittel                  | **Modular**, stufenfähig       |

### 4.4 Masse & Fertigung (parametrisch)

* **A (Längsgrade)** Gesamt-Schottfläche grob:
  $A_\text{A} \approx h_\text{deck}\cdot \Delta r \cdot N_\text{sector} \cdot N_\text{deck}$
  mit $h_\text{deck}\sim 3{,}0\,\mathrm{m}$, $\Delta r=3{,}5\,\mathrm{m}$, $N_\text{sector}=12$, $N_\text{deck}=15$ ⇒ **\~1 890 m²**.
  Masse $m \sim A\cdot t\cdot \rho$ (t=eff. Dicke; ρ\~Verbunde/Stahl).

* **B (LAT)** Flächen pro Scheibe: $A(z)=\pi\,[r_\text{out}^2(z)-r_\text{core}^2]$, Summe über **n** LAT.
  Größte Scheibe EQ (r≈63 m): $A\_\text{EQ}\approx \pi(63^2-12^2)\approx 11 600\,\mathrm{m^2}$ (als **Sandwich-Ring**, nicht Vollplatte).

* **C** Masse ≈ A + B; **t\_LAT** lässt sich gering wählen (Equalize-Philosophie, Δp≤0,2 atm), wodurch **Masse-Penalty moderat** bleibt.

---

## 5 Konsequenzen (Systemisch)

* **Design-Δp & Sequenz:** Ereignis → **radiale Sektorisierung (PT-A zu)** → **Equalize LAT** → **LAT-Portals schließen** → **VENT/BOP radial**. LAT sieht **nie Voll-Δp** (Auslegung ≤ 0,2 atm).
* **Fugen & Dämpfung:** Elastomer-Lagen an LAT-Perimeter & Sektor-Schotten senken Körperschall, nehmen Thermospannung auf.
* **ICD-Komplexität:** C erhöht Zahl definierter **Portals** (HL/PAX/UTIL) — Vorteil: **standardisierte** PT-Durchführungen, klare Prüfpfade.
* **Dynamik:** C hebt Eigenfrequenzen am stärksten → **Dock-Impulse**/Triebwerks-Response geringer; **Noise** sinkt (Scheiben als Barrieren).

---

## 6 Empfehlung / Recommendation

**Empfohlen: Variante C (Kombiniert)** als **Baseline**.

**EVOL-00 (sofort umsetzbar):**

* **12 Längsgrad-Schotten (A–L)** über DECK 001–015 (PT-A/B, AL-C wie definiert).
* **3 LAT-Scheiben:** **S40, EQ, N40** (Innenloch \~12 m, Scherstege auf Sektor-Raster, Equalizer + VENT).
  → Liefert 80–90 % des Nutzens mit moderater Masse/Komplexität.

**EVOL-01 (Upgrade):**

* Ausbau auf **7 LAT** (S56, S40, S20, EQ, N20, N40, N56), Feintuning Dämpfung, akustische Panels in LAT-Feldern.

**Fallbacks:**

* **A-only** wenn Masse/Komplexität strikt limitiert (verliert axiale Kappung/akustische Wirkung).
* **B-only** wenn radiale Schotten temporär nicht verfügbar (nicht empfohlen für Vollbetrieb).

---

## 7 Nächste Schritte / Next Steps

1. **Positions-Freeze (LAT):** z-Koordinaten, r\_out(z), Portal-Liste (HL/PAX/UTIL) je LAT.
2. **Equalizer-Sizing:** Ventquerschnitte & Zeitkonstanten, damit LAT < **0,2 atm** bleibt (Sektor-Blowout-Szenario).
3. **MEP-ICD:** Standard-PT-Durchführungen (THM/PWR/COM/GAS), Prüfklassen & Dichtkonzept.
4. **Modal-Kurzstudie:** Δ-Eigenfrequenzen & Dämpfung A vs. C; Zielwerte pro Dock/Triebwerksprofil.
5. **Massen-Budget:** t\_LON, t\_LAT, Sandwich-Kernwahl; Montage-/QC-Plan (Fugen, Bolzen-/Klebe-Gurte).

---

## 8 Anhang / Appendix (Formeln & Notizen)

* **Zentrifugalbeschleunigung:** $a(r)=\omega^2 r$; **Membranspannung Sphäre:** $\sigma \approx pR/(2t)$.
* **Mehrzellen-Torsion (Bredt-Batho):** $J \sim 4\sum A_i^2 / \sum \int \frac{ds}{t}$ — mehr Zellen ⇒ höheres *J*.
* **LAT-Geometrie:** $r_\text{out}(z)=\sqrt{R_h^2-z^2}$, $A(z)=\pi\,[r_\text{out}^2-r_\text{core}^2]$.
* **Δp-Kasten:** Radiales Schott-Segment (3,0 m × 3,5 m) bei 1,0 atm → $F\approx 1{,}06\,\mathrm{MN}$ (Bemessung Verankerung ≥ 1,1 MN).

---

## 9 Referenzen / References

* **Projekt-Spezifikationen EVOL-00** (Geometrie, Deck-Raster, Spin-Law, Safety-Philosophie).
* **Human Systems & Habitability:** NASA-STD-3001 Vol. 2 (akustik/CO₂/licht, OPS-Leitplanken).
* **Thin-walled structures & torsion:** Klassische Bredt-Batho-Theorie, multi-cell torsion design notes.
* **MMOD/Whipple & Windows:** Standards/Handbücher für LEO-Crewmodule (MDPS, Shutters).

---

### Decision Log (Sign-off)

* **Owner:** Engineer SGI Lina
* **Contributors:** Engineer Elias Core, Engineer Mara Flux
* **Decision:** *Variante C (kombiniert), EVOL-00 mit 3 LAT (S40/EQ/N40); Ausbau EVOL-01 auf 7 LAT.*
* **Date:** 2025-08-16

