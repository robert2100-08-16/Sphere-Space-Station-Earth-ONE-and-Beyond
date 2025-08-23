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
date: 2025-08-10
lang: EN
---

## AGENTS.md — Roles, Responsibilities & EVOL Working Rules

> Applies to all engineering/product docs under `7.6-engineering/...`. **EVOL** is the primary organizing principle; every activity ensures **one SSOT per topic and EVOL**.&

### A) Agents & Short Aliases (with DISC scope)

| Role / Name                  | Alias          | Primary Discipline(s) (DISC) | Systems/Scope (SYS — examples) |
| ---------------------------- | -------------- | ---------------------------- | ------------------------------ |
| Engineer **SGI Lina**        | `@sgi-lina`    | ARCH, STR                    | CORE, HULL, DECKS              |
| Engineer **Leo**             | `@eng-leo`     | OPS, TST                     | DOCK, LIFT                     |
| Engineer **Kai Nova**        | `@eng-kai`     | PROP, STR                    | PROP, CORE                     |
| Engineer **Mara Flux**       | `@eng-mara`    | PWR, THM                     | PDN, RAD                       |
| Engineer **Elias Core**      | `@eng-elias`   | SAF, REACTOR (↔ PWR)         | REACTOR, CORE                  |
| Economist **Alethea Voss**   | `@eco-alethea` | Markets / Impact             | —                              |
| Economist **Orion Hale**     | `@eco-orion`   | Investment / Impact          | —                              |
| **CFO Terra Chen**           | `@cfo-terra`   | Finance                      | —                              |
| Trade Analyst **Nova Reyes** | `@trade-nova`  | Transport / Materials        | DOCK, COMMS                    |
| **CEO Aris Vega**            | `@ceo-aris`    | Policy Gate                  | —                              |
| **COO Liora Stern**          | `@ops-lio`     | OPS                          | OPS                            |
| **CTO Jona Frame**           | `@cto-jona`    | ARCH, SW                     | CORE, COMMS                    |
| **CSO Mira Terra**           | `@cso-mira`    | SAF, ECLS                    | LHS, SAF                       |

**Codes:** DISC/SYS values follow 7.6.1.1 (ARCH, STR, THM, PWR, ECLS, SAF, GNC, PROP, OPS, ELEC, SW · CORE, HULL, DECKS, REACTOR, RAD, PDN, LHS, DOCK, LIFT, AIR, WAT, WASTE, COMMS).&

### B) Ownership Model (Owner & Reviewers)

Each document lists **Owner (DRI)** and **Reviewers** in **YAML front-matter**. Values must match the filename schema (EVOL, DISC, SYS/SYSID, LANG, STATE). **Exactly one SSOT per topic and EVOL** (state: APPROVED). &

**Owner duties**

* Technical correctness; maintain RFC/ADR/CR links; keep `supersedes/superseded_by` current.
* Keep naming, SemVer, and **STATE** consistent in filename & front-matter.
* Ensure traceability (Requirements → Interfaces → Verification).&

**Reviewer duties**

* Discipline review (DISC) + architecture/interface coherence; address risk/safety.
* Gatekeeper for **EVOL compliance** (no silent overwrites; changes via RFC/CR).&

**Minimum reviews by doc type**

* **SPEC/SRS/ICD/SAF/HAZ:** ≥ **2** — 1× discipline, 1× Arch/Safety (`@eng-elias` or `@cso-mira` or `@cto-jona`).
* **ADR:** ≥ **1** architecture review (`@cto-jona` or `@sgi-lina`).
* **RFC:** ≥ **2** (discipline + Arch/Safety) — decision recorded.
* **TST:** ≥ **1** discipline + **1** OPS (`@ops-lio`).
  These thresholds support states **DRAFT → REVIEW → APPROVED → OBSOLETE** and the SSOT rule.&

### C) EVOL Duties & Visibility

* **Badge the generation everywhere:** filenames, paths, binaries, UI “About”, dashboards, API headers, contracts, and public comms carry **EVOL-XX**.
* **One EVOL, one SSOT per topic.**
* **`current-evolution.md`** points to the active EVOL README; on freeze, archive under `7.6.3-history/EVOL-XX/...`.
* **Compare Pages** (EVOL-(N-1) ↔ EVOL-N) and **Now/Next/Later** roadmaps are auto-built.  &

### D) Workflow (Issue → Freeze)

1. **Issue/Ticket:** Problem, objective, mapping to `DOC/DISC/SYS/SYSID/DECK`.
2. **RFC** if architecture/interfaces are impacted (motivation, impact, migration, decision path).
3. **Document change** under `7.6.2-evolutions/EVOL-XX/...` with correct **filename schema** and **front-matter**.
4. **Open PR** (template below) — commit/PR titles include prefixes and **EVOL-XX**.
5. **Reviews & CI:** Lint (schema/front-matter), links, numbered tables/figures, SI units.
6. **Approval & Merge:** Set state to **APPROVED**, mark SSOT (`source_of_truth: true`).
7. **Release & Freeze:** Tag `EVOL-XX-YYYY.MM`, release notes & migration guide; freeze and archive. &

### E) Commit / PR Conventions

**Commit/PR prefix:**
`[<DOC>][<DISC>][<SYS>][<SYSID>][EVOL-XX] short summary`

**PR template**

```markdown
#### Why
(Link to Issue/RFC; motivation)

#### What
(Key changes; affected files)

#### Impact
(Compatibility, risks, migration)

#### Verification
(Tests/sims/inspections; TST IDs)

#### Links
RFC/ADR/CR/Issues

#### Checklist
- [ ] Naming & front-matter consistent (EVOL/DISC/SYS/SYSID/LANG/STATE)
- [ ] Tables/figures numbered & referenced; SI units
- [ ] RFC/ADR/TST linked
- [ ] Minimum reviews requested (see Section B)
```

Aligned with 7.6.1.1 §§8–10 and CI rules.&

### F) Quality Gates (CI/Lint) & Merge Blockers

* **Hard lint checks:**

  * EVOL in path == EVOL in filename; regex schema satisfied.
  * Front-matter ↔ filename consistency (`id`, `evolution`, `discipline`, `system`, `system_id`, `seq`, `lang`, `state`).
  * SemVer valid; `STATE` consistent in name & front-matter.
* **Blockers:** missing reviews, broken RFC/ADR/CR links, wrong SemVer, stale `supersedes/superseded_by`.&

### G) Governance & Decisions (EVOL Board)

* **Open a new EVOL** only for **system-wide architectural breaks** / unshimmable interface breaks / changed ops doctrine.
* Submit request via **RFC** with impact analysis, migration, and customer narrative; board review (Architecture, Safety, Ops, Finance, Programs).
* **Freeze & fork forward:** freeze EVOL-N (read-only/patch-only), continue development in EVOL-(N+1).&

**Escalation**

* Cross-discipline conflict: moderation by `@cto-jona` (Architecture) + `@cso-mira` (Safety/Sustainability).
* Time-critical/Safety-critical: ad-hoc board (`@cto-jona`, `@eng-elias`, `@cso-mira`, Owner).&

### H) Role-Specific Responsibilities (excerpt)

* **@cto-jona (Architecture Gate):** architecture compliance, ADR index, EVOL-change gatekeeper.&
* **@cso-mira / @eng-elias (Safety Gate):** SAF/HAZ dossiers, ops doctrine, EVOL support windows.&
* **@ops-lio (Ops Gate):** SOPs, operations/maintenance chapters, VVP/V\&V coverage.&
* **@sgi-lina (Systems/STR):** structure/ICD coherence, Req↔Verification traceability.&
* **@eng-mara (PWR/THM):** energy/thermal flows, EVOL compare pages for PWR/THM ICDs.&
* **@eng-kai (PROP):** propulsion interfaces, migration paths for thrust/power changes.&
* **@eng-leo (OPS/TST):** test plans/reports, conformance (TST) ↔ SPEC/ICD.&
* **@cfo-terra / @eco-orion / @eco-alethea / @trade-nova (Economics/Transport):** release/freeze gates, support policy, migration cost awareness.&

### I) Quick Cheat Sheet

* **New SPEC?** → Filename per schema, fill YAML, link RFC, collect **2 reviews**, set state.&
* **Small fix?** → **PATCH** bump; semantic changes = **MINOR/MAJOR** (within the EVOL).&
* **Architectural break?** → RFC → Board → maybe **new EVOL**; freeze the old EVOL.&
* **Release?** → Tag `EVOL-XX-YYYY.MM`, release notes + migration guide, verify `current-evolution.md`, publish compare pages. &

### Appendix 1: Filename Schema & Front-Matter (Quick Ref)

**Filename**
`<DOC>-<EVOL>-<DISC>-<SYS>-<SYSID>-<SEQ>-<TITLE>-<LANG>-v<MAJOR.MINOR.PATCH>[<PRERELEASE>][+<BUILD>][-<STATE>].md`
Allowed fields/states/regex see 7.6.1.1 §§4–6 & §13. &

**Front-matter (required)**
`id, title, version, state, evolution, discipline, system, system_id, seq, owner, reviewers, source_of_truth, supersedes, superseded_by, rfc_links, adr_links, cr_links, date, lang` — values must match the filename.&

### Appendix 2: Example PR Title

```
[SPEC][STR][DECKS][DECK000][EVOL-01] hatch tolerances v1.1.0
```

Conforms to 7.6.1.1 §8 examples.&

### Validity & Maintenance

This document is the **SSOT** for roles/workflows in EVOL contexts. Changes via **RFC** only; approval by Architecture/Safety/Ops gates. Show the active EVOL badge in the header and maintain the EVOL README.&

---


