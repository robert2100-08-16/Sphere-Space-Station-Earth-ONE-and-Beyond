# 7.6 Engineering

This folder is the engineering workspace for **Sphere Space Station Earth ONE and Beyond**. It hosts our standards, working “Evolutions” (EVOLs), specs, models, tests, operational procedures, and the auditable history that ties decisions to evidence. Treat this directory as part of the Single Source of Truth (SSOT).

---

## What lives here

* **AGENTS.md** – Roles, ownership model, EVOL duties & visibility, workflow, commit/PR conventions, quality gates, and governance. Use this to know who owns what and how work flows from **Issue → Freeze**.
* **7.6.1 Global Standards** – Our core playbooks:

  * *Evolution-Engineering Naming & Folder Convention* (file layout, filename schema, required front-matter, versioning, doc states, automation hooks).
  * *The Evolution Principle* (why we work in small, reviewable EVOLs).
  * *Evolution Deliverables & Phase Gates* (what must exist at each stage, with checklists).
* **7.6.2 Evolutions** – Active and archived EVOLs, each with its own scope, templates, CI rules, and contribution checklist. The current seed is **EVOLUTION 00 – The Beginning**.
* **7.6.3 History** – Snapshots, freezes, and decision records that give us traceability over time.

---

## Quick start (for contributors)

1. **Read `AGENTS.md`.** Find the *Owner* and *Reviewers* for your area; understand merge blockers and visibility rules.
2. **Pick or open an EVOL.** Work happens inside an EVOL (e.g., `EVOL-00/`), not loose in the root. Each EVOL carries its own scope, templates, and CI expectations.
3. **Create files using the standard schema** (see *Global Standards → Naming & Folder Convention*). Add the required YAML front-matter before content.
4. **Open a PR** following the title/commit rules in `AGENTS.md`. Expect lint, schema, link, and glossary checks to run; fix all CI findings.
5. **Pass the gate.** Reviews map to our phase gates (SRR/SDR/PDR/CDR/TRR/QR/FAR/ORR). Your EVOL’s checklist defines the minimal evidence required to advance.

---

## Folder layout (at a glance)

```
7.6-engineering/
├─ AGENTS.md
├─ 7.6.1-global-standards/
│  ├─ evolution-engineering-naming-folder-convention.md
│  ├─ the-evolution-principle.md
│  └─ evolution-deliverables-and-phase-gates.md
├─ 7.6.2-evolutions/
│  ├─ EVOL-00/
│  │  ├─ readme.md
│  │  ├─ 00-standards-templates/
│  │  ├─ 01-architecture/
│  │  ├─ 02-specs/
│  │  ├─ 03-interfaces/
│  │  ├─ 04-calculations/
│  │  ├─ 05-models-cad-sim/
│  │  ├─ 06-tests-verification/
│  │  ├─ 07-ops-maintenance/
│  │  └─ 08-change-management/
└─ 7.6.3-history/
```

Each EVOL folder carries the same skeleton so artifacts are predictable and traceable.

---

## File naming & versioning (must-do)

Use the governed pattern from *Global Standards*:

```
<DOC-TYPE>-<EVOL>-<DISC>-<DOMAIN>-<ID>-<subject>-<LANG>-v<SemVer>-<STATE>.md
```

**Example** (already in this repo):
`SPEC-00-STR-DECKS-DECK000-0001-wormhole-docking-tunnel-EN-v0.1.0-DRAFT`
Where:

* `DOC-TYPE` = SPEC/RFC/ICD/TEST/OPS…
* `EVOL` = two digits (e.g., 00)
* `DISC` = discipline tag (e.g., STR, THM, ECLSS, GNC)
* `SemVer` = `MAJOR.MINOR.PATCH`
* `STATE` = DRAFT → REVIEW → APPROVED → FROZEN (plus DEPRECATED when retired)

Front-matter is **required** (owner, reviewers, EVOL, discipline, status, links to requirements/tests). CI will block missing or malformed headers.

---

## Evolution lifecycle & phase gates

We design **coarse → fine**, proving feasibility early, then tightening evidence through gates. Typical gates used across EVOLs:

* **SRR** – System Requirements Review
* **SDR/AR** – Architecture Review
* **PDR** – Preliminary Design Review
* **CDR** – Critical Design Review
* **TRR** – Test Readiness Review
* **QR/FAR** – Qualification / Flight Acceptance Review
* **ORR** – Operations Readiness Review

Each gate has minimal deliverables (documents, models, tests, checklists) defined in *Evolution Deliverables & Phase Gates*. Merge is blocked until the gate’s checklist is satisfied.

---

## CI, quality gates, and merge blockers

Every PR runs automated checks for:

* Filename & front-matter schema compliance
* Link integrity & cross-references
* Glossary/abbreviation use
* Lint/format rules per document type
* Required attachments (evidence, ICDs, test matrices) for the current gate

Failing any check blocks merge. Owners/Reviewers enforce additional domain-specific criteria as defined in `AGENTS.md`.

---

## Working in an EVOL

1. Start with the EVOL’s `readme.md` to confirm scope and open questions.
2. Add/change artifacts only inside that EVOL’s skeleton (`01-architecture`, `02-specs`, `03-interfaces`, …).
3. Use SemVer and update **STATE** as your document advances (DRAFT → REVIEW → APPROVED → FROZEN).
4. Record context in `08-change-management/` so history remains auditable.

---

## Example: active seed evolution

* **EVOLUTION 00 – The Beginning**
  Includes early geometry/material baselines and first SPECs such as the **Wormhole Docking Tunnel** (ID `DECK000-0001`). Use it as a pattern for structure, naming, and evidence packaging.

---

## Governance & decisions

The **EVOL Board** arbitrates cross-cutting decisions and freezes. Day-to-day ownership and reviewer responsibilities are defined in `AGENTS.md`. If in doubt about scope, naming, or gate content—ask the Owner listed in the document front-matter before you branch.

---

## Related foundations

For system-wide engineering flow (from concept through operations), see **7.5.1 Engineering Process (Coarse → Fine)**; it aligns with the gates and artifacts referenced here and explains how requirements map to verification and operational evidence.

---

**License & IP** – See the root project notices for rights, usage, and compliance requirements. All contributions to 7.6 must remain auditable and traceable to requirements and reviews.

---

*You’re in the right place to build flight-worthy things. Keep it small, reviewable, and evidence-backed.*
