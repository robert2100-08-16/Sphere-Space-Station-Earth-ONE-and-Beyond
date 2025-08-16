---
id: spec-00-str-decks-deck000-0001
title: DECK000 wormhole docking tunnel
version: 0.1.0
state: draft
evolution: EVOL-00
discipline: STR
system: DECKS
system_id: "DECK000"
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
date: 2025-08-10
lang: en-de
---

# SPEC-00-STR-DECKS-DECK000-0001-wormhole-docking-tunnel-EN-DE-v0.1.0-DRAFT

**The Engineering of DECK000 – The Wormhole**

**Document status:** Draft (EVOL-00 baseline)
**Date:** 2025‑08‑10
**Applies to:** Earth ONE class sphere station (Ø 127 m)

---

## Summary / Kurzfassung (EN/DE)

**EN:** DECK000 is the axial, pressurized docking and transit tube spanning the North–South poles. The EVOL-00 baseline defines a 127 m long SiC-composite barrel with six Inconel docking rings and window segments for observation and transfer in micro‑g.

**DE:** DECK000 ist der axiale, druckbeaufschlagte Docking- und Transittunnel zwischen Nord- und Südpol. Die EVOL‑00-Basis umfasst einen 127 m langen SiC-Verbundzylinder mit sechs Inconel-Docking-Ringen und Fenstersegmenten für Beobachtung und Transfer im Mikro-g.

---

#### 1 Abstract


DECK000 (“The Wormhole”) is the axial, pressurized docking and transit tube that runs straight through the station from the North pole to the South pole. In EVOL‑00, the assembly is a 127 m long tube with an outer diameter of 22 m and a clear inner diameter of 20 m. The primary barrel is a silicon‑carbide (SiC) composite reinforced with steel or Inconel for toughness. Starting 3.5 m from the north polar end and repeating every 20 m along the axis, 10 m‑long Inconel docking‑ring subassemblies are installed and numbered sequentially (00, 01, 02 …) from North to South. Between docking rings, “window tube” segments provide outward viewing; each segment integrates rectangular window units of 4 m (axial) × 3 m (tall), built to the program’s space‑grade multilayer window specification (ALON/sapphire + fused silica + polycarbonate + borosilicate/cerium‑doped glass). The result is a micro‑g corridor (near the spin axis) enabling safe berthing, people/cargo transfer, observation, and emergency egress.

---

#### 2 Description (EVOL‑00 – Baseline Geometry & Materials)

##### A. System Overview

* **Function:** Central polar docking, transit, and observation corridor in micro‑g; houses guidance, lighting, utilities, and emergency isolation points.
* **Overall length:** 127 m (North pole interior face to South pole interior face).
* **Primary diameters:** OD 22 m; ID 20 m (clear).
* **Primary structure:** SiC composite barrel; local reinforcement with steel/Inconel where penetrations, hatches, or docking hardware concentrate loads.
* **Environment:** Pressurized to station nominal (TBC; baseline 1 atm); micro‑g zone due to proximity to rotation axis.

##### B. Docking‑Ring Architecture

* **Ring modules:** 10 m axial length; OD 22 m (flush with main barrel OD); ID 10 m (constricted throat for docking hardware and hatchway integration).
* **Material:** Inconel (high‑temperature and corrosion resistance; excellent toughness).
* **Placement & numbering:** Starting **3.5 m** from the North pole interior face and repeating at a **20 m pitch**; numbered **00** (northmost) through **05** (southmost) in EVOL‑00.

**Table 1 — Ring and window‑segment positions (from North pole interior face)**

| Segment | Type         | Axial start (m) | Axial end (m) | Axial length (m) | Notes                               |
| ------: | ------------ | --------------: | ------------: | ---------------: | ----------------------------------- |
|       — | Clearance    |             0.0 |           3.5 |              3.5 | forward clearance / taper / systems |
|      00 | Docking ring |             3.5 |          13.5 |             10.0 | Inconel ring ID 10 m                |
|       — | Window tube  |            13.5 |          23.5 |             10.0 | window segment                      |
|      01 | Docking ring |            23.5 |          33.5 |             10.0 |                                     |
|       — | Window tube  |            33.5 |          43.5 |             10.0 |                                     |
|      02 | Docking ring |            43.5 |          53.5 |             10.0 |                                     |
|       — | Window tube  |            53.5 |          63.5 |             10.0 |                                     |
|      03 | Docking ring |            63.5 |          73.5 |             10.0 |                                     |
|       — | Window tube  |            73.5 |          83.5 |             10.0 |                                     |
|      04 | Docking ring |            83.5 |          93.5 |             10.0 |                                     |
|       — | Window tube  |            93.5 |         103.5 |             10.0 |                                     |
|      05 | Docking ring |           103.5 |         113.5 |             10.0 |                                     |
|       — | Window tube  |           113.5 |         123.5 |             10.0 |                                     |
|       — | Clearance    |           123.5 |         127.0 |              3.5 | aft clearance / taper / systems     |

> **Note:** EVOL‑00 uses six docking rings (00–05), preserving 3.5 m service clearances at both ends. Later evolutions may revise counts, spacing, or diameters based on interface selections and docking traffic models.

##### C. Window Segments & Glazing Units

* **Window units per segment:** Rectangular apertures integrated into the 10 m “window tube” spans; count and circumferential distribution TBD by human‑factors and structural analyses.
* **Nominal window aperture:** 4.0 m (axial) × 3.0 m (tall / meridional).
* **Glazing stack (per program spec):**

  * Outer strike face: **ALON** (or sapphire) \~50 mm for micrometeoroid & UV protection.
  * Middle layers: **Fused silica** (\~100 mm) + **polycarbonate** (\~50 mm) for thermal stability and impact energy absorption.
  * Inner layer: **Borosilicate** (or cerium‑doped glass) \~30 mm for radiation attenuation and optical quality.
  * **Total thickness:** \~200–300 mm; **areal mass:** \~530–550 kg/m².
* **Shutters & shields:** Each aperture integrates internal blast shutters and external micrometeoroid/thermal shades; automatic closure on pressure loss or debris alerts.

##### D. Structural Concept

* **Primary barrel wall:** Thickness TBD from combined loads (pressure, docking loads, thermal gradients). Preliminary design envelope to meet FoS ≥ 2.0 against yield under 1 atm differential plus ring‑induced stress concentrations.
* **Ring‑to‑barrel joints:** Circumferential flanges with shear keys; dual redundant, high‑temperature elastomer seals (silicone‑based) with metallic C‑seals for vacuum‑rated redundancy.
* **Local reinforcements:** Around windows (doubler frames), utility penetrations, and docking hardware. Use SiC/steel hybrid frames to spread aperture loads into the barrel laminate.
* **Thermal control:** Embedded liquid heat loops (glycol‑water or silicone oil), MLI blankets on the outside of the barrel segments not occupied by windows, and conductive paths to station radiators.

##### E. Interfaces & Services

* **Mechanical:** Hard‑points in each docking ring for adapter hardware, hatches, grapples, and temporary airlocks.
* **Avionics & comms:** Redundant comm rails, guidance beacons, and visual docking aids integrated at each ring; cableways routed in protected trunking.
* **Life support:** Distributed air distribution manifolds, CO₂ scrubber returns, water/condensate drains, and emergency O₂ drop lines.
* **Power:** Dual independent DC buses along the tube with local UPS for shutters, lighting, and hatch actuators.
* **Safety:** Pressure‑isolation bulkheads at ring boundaries (ring can be sealed as a compartment), blast doors for window segments, fire detection & inert‑gas suppression.

##### F. Operations & Human Factors

* **Micro‑g ergonomics:** Handrails, foot restraints, and guided translation lines throughout; lighting graded for approach/egress; color‑coded wayfinding matching station standards.
* **Traffic separation:** North pole dedicated to arrivals, South pole to departures (baseline); center‑tube signage and beacons enforce counter‑flow.
* **Emergency egress:** Clearly marked safe‑hold nodes at each ring with comms, masks, and emergency supplies; shutters auto‑close upon hazard detection.

##### G. Manufacturing & Assembly

* **Moduleization:** 10 m modules (alternating ring modules and window‑tube modules) pre‑fitted with internal systems; on‑orbit assembly via circumferential bolted/bonded joints.
* **Inspection & maintenance:** Ring‑module inspection ports; replaceable shutter cassettes; window health monitoring (acoustic emission, strain gauges, optical clarity sensors).

##### H. Compliance & Reference Specs

* Materials, pressure vessels, fire, glazing, and MMOD protections comply with station‑wide standards (refs). Window stacks must meet the program’s “LEO Window Specification” for thermal cycling, rapid decompression, and micrometeoroid resistance.

##### I. Open Parameters (TBD/TBC)

* Barrel wall thickness and detailed layup by load case.
* Final ring inner diameter vs. docking system selection and hatch design.
* Window count/distribution per segment after view/structure trade.
* Detailed thermal loop routing and radiator tie‑ins.
* Human‑factors lighting and signage specifics.

---

#### 3 Forward Work (next revision)

1. Complete pressure & docking load cases and size the barrel thickness and reinforcements.
2. Human‑factors layout (window count/placement, handrail nets, signage).
3. Define ring‑module interface for standardized docking adapters.
4. Hazard analysis (fire, decompression) and emergency procedure overlays.
5. Manufacturing tolerances, NDI plan, and acceptance criteria.
