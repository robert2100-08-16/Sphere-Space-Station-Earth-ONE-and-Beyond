# Guideline Document: Engineering Naming & Folder Convention
**Version:** 1.0.0
**Date:** 2025-08-10

> Goal: Traceable, machine-sortable, version-safe documentation for a large-scale project. This convention defines folder structure, file names, versioning, states, role references, and cross-linking.

---

## 1) Scope & Core Principles

**Scope:** all files under `7.6-engineering/` (work-in-progress) and `7.6.1-history/` (frozen).

**Principles:**

* **SSOT:** Single Source of Truth – exactly one approved reference document per topic.
* **Traceability:** Every claim (SPEC/SRS) leads to interfaces (ICD) and tests (TST) that reference it.
* **Readability & Sortability:** Short codes, fixed order, leading zeros, ISO date, SemVer.
* **Stability:** Codes for disciplines/systems are maintained in tables (see below); changes only via RFC.

---

## 2) Folder Structure (Top-Down)

```text
7.6-engineering/
├─ 7.6.1-history/                 # frozen, superseded states
└─ 7.6.2-current-engineering/     # current working state
   ├─ 00-standards-templates/     # naming scheme, templates, ADR/RFC format
   ├─ 01-architecture/            # system architecture, ADRs
   ├─ 02-specs/                   # specifications (SRS, SPEC, ICD, SAF ...)
   ├─ 03-interfaces/              # mechanical/electrical/software, ports/signals
   ├─ 04-calculations/            # spreadsheets, substantiation
   ├─ 05-models-cad-sim/          # CAD, FEM/CFD/simulation models
   ├─ 06-tests-verification/      # V&V, test plans/reports, acceptance
   ├─ 07-ops-maintenance/         # operations, maintenance, SOPs
   └─ 08-change-management/       # RFC/CR/Approvals (referenced by all docs)
```

**README per folder** includes: purpose, index, mandatory links (relevant ADR/RFC/TST).

---

## 3) File-Naming Scheme

```text
<DOC>-<EVOL>-<DISC>-<SYS>-<DECK>-<ID>-<TITLE>-<LANG>-v<MAJOR.MINOR.PATCH>[<PRERELEASE>][+<BUILD>][-<STATE>].md
```

**Field definitions:**

* `DOC` (document type): **SPEC**, **SRS**, **ICD**, **ADR**, **RFC**, **CR**, **TST**, **CALC**, **DRAW**, **BOM**, **SOP**, **SAF** (safety analysis), **HAZ** (HAZOP/FMEA), **VVP** (Verification & Validation Plan).
* `EVOL` (evolution line): **00** (baseline), **01**, **02** … (architecture generation).
* `DISC` (discipline): **ARCH**, **STR**, **THM**, **PWR**, **ECLS**, **SAF**, **GNC**, **PROP**, **OPS**, **ELEC**, **SW**.
* `SYS` (system/subsystem, examples): **CORE**, **HULL**, **DECKS**, **REACTOR**, **RAD** (radiators), **PDN** (Power Distribution Network), **LHS** (Liquid Heat Storage), **DOCK**, **LIFT**, **AIR** (atmosphere), **WAT** (water), **WASTE**, **COMMS**.
* `DECK` (deck reference): **DECK000** … **DECK015**, or **ALL** (cross-deck).
* `ID` (sequential number per combination): **0001**, **0002** …
* `TITLE` (kebab-case, 6–8 words max).
* `LANG`: **DE**, **EN**.
* `v<MAJOR.MINOR.PATCH>`: **SemVer** (see Section 4).
* `<PRERELEASE>` (optional): `-alpha.1`, `-beta.2`, `-rc.1`.
* `+<BUILD>` (optional): e.g., `+20250810`, `+git.abcdef`.
* `STATE` (optional, work/approval status): **DRAFT**, **REVIEW**, **APPROVED**, **OBSOLETE**.

**Examples:**

```text
SPEC-00-STR-DECKS-DECK000-0001-wormhole-docking-tunnel-EN-v1.0.0-DRAFT.md
ICD-00-THM-RAD-ALL-0044-radiator-icd-ports-DE-v1.3.0-REVIEW.md
ADR-00-ARCH-CORE-ALL-0003-spin-rate-baseline-EN-v1.0.0.md
RFC-00-SAF-REACTOR-DECK015-0007-shielding-upgrade-EN-v0.3.0-alpha.2.md
```

---

## 4) Versioning (SemVer) & Document States

**SemVer:** `MAJOR.MINOR.PATCH`

* **MAJOR:** fundamental/incompatible change to the subject matter (new architecture generation, replaced assumptions, changed interface semantics). Requires a **new evolution line** or a **supersedes** note.
* **MINOR:** backward-compatible additions (new section, additional requirements, non-breaking clarifications).
* **PATCH:** purely editorial/small corrections (typos, layout, minor wording without change of meaning).
* **Prerelease:** `-alpha.N`, `-beta.N`, `-rc.N` until release.
* **Build:** `+YYYYMMDD` or `+git.<shortsha>` optional.

**States:**

* **DRAFT** → **REVIEW** (min. 2 reviews) → **APPROVED** (reference as SSOT) → **OBSOLETE** (replaced by successor).
* When moving to **APPROVED**, an RFC/CR must exist and be linked.

---

## 5) Front Matter (Required)

Every file starts with YAML front matter:

```yaml
---
id: SPEC-00-STR-DECKS-DECK000-0001
title: Wormhole Docking Tunnel – Structural Specification
version: v1.0.0
state: DRAFT
owner: @sgi-lina
reviewers: [@saf-core, @ops-lio]
source_of_truth: true
supersedes: null
superseded_by: null
rfc_links: [RFC-2025-0007]
adr_links: [ADR-00-ARCH-CORE-ALL-0003]
date: 2025-08-10
lang: EN
decks: [DECK000]
systems: [DECKS]
discipline: STR
---
```

---

## 6) Change Management

* **RFC ID:** `RFC-YYYY-####` (e.g., `RFC-2025-0007`). Content: change, motivation, impact, migration plan, participants, decision.
* **CR ID:** `CR-YYYY-####` for concrete implementation packages.
* **Process:** Issue → RFC (review) → decision → implementation (CR/PR) → update documents → test/acceptance → status change.
* **Supersedes maintenance:** Old document gets `superseded_by`, new document gets `supersedes`. The older one moves to `7.6.1-history/`.

---

## 7) Commit Messages & PR Titles

**Format:**

```
[<DOC>][<DISC>][<SYS>][<DECK>] short summary

Body:
- why: motivation/issue link
- what: key changes
- impact: backward compat / risks
- refs: RFC/ADR/CR IDs
```

**Example:**

```
[SPEC][STR][DECKS][DECK000] define hatch tolerances v1.1.0

why: close gaps from TST-... results
what: ±0.2 mm tolerance band, updates figures 2–4
impact: compatible; requires retest case 2
refs: RFC-2025-0009, ADR-00-ARCH-CORE-ALL-0003
```

---

## 8) CODE Tables (extendable via RFC only)

### 8.1 Disciplines (`DISC`)

* ARCH – Architecture/System
* STR – Structures/Mechanics
* THM – Thermal
* PWR – Energy/Power
* ECLS – Life Support
* SAF – Safety
* GNC – Guidance, Navigation & Control
* PROP – Propulsion
* OPS – Operations
* ELEC – Electrical/ELEC
* SW – Software

### 8.2 Systems (`SYS`) – Selection

* CORE, HULL, DECKS, REACTOR, RAD, PDN, LHS, DOCK, LIFT, AIR, WAT, WASTE, COMMS

### 8.3 Deck IDs (`DECK`)

* DECK000 … DECK015; **ALL** for cross-deck

---

## 9) Templates (Short Forms)

> Detailed templates are located in `7.6.2-current-engineering/00-standards-templates/`.

### 9.1 SPEC Template (Markdown)

```markdown
---
# (YAML front matter as above)
---

# 1. Purpose & Context
# 2. Scope
# 3. Terms & References
# 4. Requirements (numbered: SPEC-REQ-001 …)
# 5. Constraints & Assumptions
# 6. Verification (mapping SPEC-REQ → test cases)
# 7. Risks & Safety Notes
# 8. Change History
```

### 9.2 ICD Template

```markdown
---
# (YAML front matter)
---

# 1. Interface Overview
# 2. Mechanical (coordinates, tolerances, drawings)
# 3. Electrical (pins, voltages, signals)
# 4. Software/Protocol (frames, timing)
# 5. States & Failure Cases
# 6. Tests (conformance)
# 7. Change History
```

### 9.3 ADR Template

```markdown
---
# (YAML front matter)
---

# Context
# Decision
# Consequences
# Alternatives
# References (RFC, SPEC)
```

### 9.4 RFC Template

```markdown
---
# (YAML front matter)
---

# Problem & Motivation
# Proposal (high level)
# Impact (technology, risk, cost)
# Compatibility & Migration
# Review Plan & Owner
# Decision (date, participants)
```

### 9.5 TST Template (Test Report)

```markdown
---
# (YAML front matter)
---

# Test Objective
# Test Environment
# Test Cases (ID, step sequence, expectation)
# Results & Evidence
# Deviations/Non-Conformities
# Conclusion & Approval
```

### 9.6 CALC Template

```markdown
---
# (YAML front matter)
---

# Assumptions & Parameters (with sources)
# Derivation/Methodology
# Calculation Steps (formulae, units)
# Results (tables/graphs)
# Sensitivity & Uncertainties
# Correlation with Measurement/Simulation
```

---

## 10) Quality Rules (Short)

* One topic per document; split and cross-link large topics.
* Number tables/figures and reference them in the text.
* SI units, decimal point, fixed prefixes (k, M, µ …).
* All numbers with source/derivation; charts with axis labels & units.
* Every change traceable via RFC/CR; no “silent” overwrites.

---

*End of document.*
