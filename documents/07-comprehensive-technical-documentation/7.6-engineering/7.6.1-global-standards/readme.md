# 7.6.1 Global Standards

Welcome! This folder defines the **project-wide rules** for how we name, version, structure, review, and ship every document in the Sphere Space Station *Earth ONE & Beyond* Single Source of Truth (SSOT). If you’re writing a spec, an interface control document, an ADR, an RFC, a test report, or a calculation note, **start here**.

---

## What lives here

* **Scope & Core Principles** — Why these standards exist and where they apply.
* **Folder Structure (top-down)** — How the SSOT is organized so content is discoverable and auditable.
* **Evolution Lifecycle** — From idea → draft → review → *freeze*; how documents mature alongside engineering work.
* **File-Naming Scheme** — A strict, machine-checkable pattern so docs are traceable and linkable.
* **Versioning & Document States** — SemVer + explicit states (e.g., `DRAFT`, `…`, `FROZEN`) to signal readiness.
* **Required YAML Front Matter** — The minimal metadata every file must declare.
* **Change Management** — How updates are proposed, reviewed, and recorded.
* **Commit Messages & PR Titles** — Conventions that feed automation and release notes.
* **CODE Tables** — Controlled vocabularies (document types, disciplines, systems, decks, states).
* **Templates** — Short, ready-to-use markdown stubs (SPEC, ICD, ADR, RFC, TST, CALC).
* **Quality Rules & CI/Lint** — Automated checks (regex, cross-refs, state transitions) that gate merges.

> The outline above corresponds to the “7.6.1 — Global Standards” section in the master documentation.

---

## Quick start

1. **Pick the right template** (SPEC / ICD / ADR / RFC / TST / CALC) from this folder’s `templates`. Each template maps to a **DOC** code in the CODE tables.
2. **Name your file** using the standard pattern below.
3. **Add required YAML front matter** (see sample + Appendix 14.3 for the full field list).
4. **Open a PR** with a compliant title; CI will lint filenames, front-matter, and cross-links.
5. Drive it through the **Evolution Lifecycle** until the document reaches the intended **state**.

---

## One last thing

When in doubt: **prefer traceability over brevity**. If your change affects safety, mission, budgets, or interfaces, make the intent obvious—in the filename, in the front-matter, and in the PR. The standards here exist so that every critical decision is **auditable, reproducible, and evolvable**.
