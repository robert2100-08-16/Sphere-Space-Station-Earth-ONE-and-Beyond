# 7.6.2 Evolutions

This folder contains the **active engineering “Evolution” packages** for the Sphere Space Station Earth ONE and Beyond project. Each Evolution groups the current set of specs, interfaces, calculations, models, tests, and ops procedures that together define the system **as it is being changed right now**. Older waves move to `7.6.3 History`.

---

## What’s in here

* **Current Evolution(s)** — the live development wave(s) with their documents and work-in-progress artifacts. For example, the book lists **EVOLUTION 00 — The Beginning** as the starting wave.
* **Specs under this Evolution** — e.g.,
  `SPEC-00-STR-DECKS-DECK000-0001-wormhole-docking-tunnel-EN-v0.1.0-DRAFT` (structure, decks, DECK000, EN locale, SemVer + state).

Each Evolution typically mirrors the reference layout used in the history section (standards/templates, architecture, specs, interfaces, calculations, models/sim, tests, ops, change management). When an Evolution closes, its content is frozen and archived to `7.6.3 History` (e.g., `EVOL-00/00-standards-templates`, `01-architecture`, `02-specs`, …).

---

## How Evolutions work (fast primer)

* **Evolution principle & lifecycle**: Evolutions are small, visible, and governed. They move from proposal → work → review → freeze, following the rules and lifecycle defined in **7.6.1 Global Standards** and **Guideline Document: The Evolution Principle**.
* **Governance & roles**: See **AGENTS.md — Roles, Responsibilities & EVOL Working Rules** for owners, reviewers, EVOL board decisions, and merge blockers.

---

## File naming, versioning, and states

Follow the **7.6.1 Global Standards** rigorously:

* **File-Naming Scheme** (document type, evolution code, discipline, system/deck IDs, language, SemVer, state).
  Example: `SPEC-00-STR-DECKS-DECK000-0001-…-EN-v0.1.0-DRAFT`.
* **Versioning**: **SemVer** (`MAJOR.MINOR.PATCH`). Increase versions per the change impact; keep states in sync.
* **Document States**: e.g., `DRAFT` → `REVIEW` → `FROZEN` (see “States (STATE)” code table).
* **Required YAML front matter**: include required metadata (doc type, evolution, owners, reviewers, state, version, etc.). CI will check this.

---

## Templates you’ll need

Short-form templates are provided for **SPEC, ICD, ADR, RFC, TST, CALC**. Start from these when adding documents to this Evolution.

---

## CI, quality gates, and merge rules

* **Quality rules & CI/Lint**: Filename regex, front-matter fields, and cross-checks are enforced. Fix issues before requesting review.
* **Commits & PRs**: Use the prescribed **commit message and PR title conventions** so traceability stays intact. Merge is blocked until reviews and checks pass per **EVOL board** rules.

---

## Contributing to this Evolution (checklist)

1. **Create/extend docs** using the correct **template + filename + front matter**.
2. **Reference codes/tables** (DOC types, DISC, SYS, DECK IDs, STATE) from the standards appendix.
3. **Run CI locally** where possible; fix lint and metadata errors.
4. **Open a PR** with compliant title/description; request the listed **owners/reviewers** in `AGENTS.md`.
5. **Address reviews**; once approved and CI is green, the EVOL board (or delegate) merges. **Frozen artifacts** will later be copied to `7.6.3 History` as the next wave starts.

---

## Quick pointers

* **Global standards & lifecycle, versioning, states, front matter, CI/Lint** → `7.6.1-global-standards` and **Guideline: The Evolution Principle**.
* **Roles, ownership, workflows** → `7.6-engineering/AGENTS.md`.
* **History and prior waves** → `7.6.3 History` (e.g., `EVOL-00` structure for reference).
* **Example active spec** → wormhole docking tunnel spec listed under EVOLUTION 00.

---

## Scope reminder

This folder is the **single source of truth for the *current* change wave**. If it’s not here (or linked from here), it’s not part of the active Evolution. Archive only after freeze; until then, keep everything auditable, versioned, and governed.

---

*Maintainers:* See `AGENTS.md` for the current Evolution owner(s) and reviewer roster.

