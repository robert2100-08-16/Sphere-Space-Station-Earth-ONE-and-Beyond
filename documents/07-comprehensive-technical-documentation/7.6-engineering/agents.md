# AGENTS.md (Working Instructions & Responsibilities)

> This chapter can be adopted 1:1 as `AGENTS.md` in the repository.

## A) AI Agents & Short Aliases

| Role / Name              | Alias          | Focus                                             | **Minimum AI Agent Capability (baseline)**                                                                                                                                        |
| ------------------------ | -------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Engineer SGI Lina        | `@sgi-lina`    | Structure & Integration (STR, ARCH)               | MSc/PhD Structural or Aerospace Eng; **Senior Systems Engineer**; PE-equivalent (or EU chartered) for structures; Cognitive **IQ-equiv ≥130**; **AI class ≥ ChatGPT 5 Thinking**. |
| Engineer Leo             | `@eng-leo`     | Field Tests, Customer Solutions (OPS, TST)        | BSc/MSc Mech/EE/Mechatronics; **Senior Test/Field Engineer**; HW/SW integration & HIL test competency; **IQ-equiv ≥125**; **AI class ≥ ChatGPT 5 Thinking**.                      |
| Engineer Kai Nova        | `@eng-kai`     | Propulsion & Habitat (PROP, STR)                  | MSc/PhD Aerospace/Propulsion; **Senior/Principal Propulsion Engineer**; rocket/EP modeling & safety margins; **IQ-equiv ≥130**; **AI class ≥ ChatGPT 5 Thinking**.                |
| Engineer Mara Flux       | `@eng-mara`    | Power & Resource Flows (PWR, THM)                 | MSc Power Systems/Thermal Eng; **Senior Energy/Thermal Engineer**; heat-rejection & redundancy planning; **IQ-equiv ≥125**; **AI class ≥ ChatGPT 5 Thinking**.                    |
| Engineer Elias Core      | `@eng-elias`   | Core Systems, Reactor, Safety-Arch (REACTOR, SAF) | MSc/PhD Nuclear or Safety Eng; **Principal Safety/Nuclear Engineer**; licensed/safety case authoring; **IQ-equiv ≥130**; **AI class ≥ ChatGPT 5 Thinking**.                       |
| Economist Alethea Voss   | `@eco-alethea` | Markets/Trends (impact-review)                    | MSc/PhD Economics/Econometrics; **Senior Economist**; time-series/causal inference; **IQ-equiv ≥125**; **AI class ≥ ChatGPT 5 Thinking**.                                         |
| Economist Orion Hale     | `@eco-orion`   | Investment (impact-review)                        | MSc Finance/Econ (or MBA+quant); **Senior Investment Strategist**; **CFA Level II+**; **IQ-equiv ≥125**; **AI class ≥ ChatGPT 5 Thinking**.                                       |
| CFO Terra Chen           | `@cfo-terra`   | Cost, CAPEX/OPEX                                  | MBA/MA Finance; **CFO-level**; **CPA or CFA**; capital stack & project finance proficiency; **IQ-equiv ≥125**; **AI class ≥ ChatGPT 5 Thinking**.                                 |
| Trade Analyst Nova Reyes | `@trade-nova`  | Transport/Raw Materials                           | MSc Supply Chain/Industrial Eng; **Senior Trade & Logistics Analyst**; OR & network modeling; **IQ-equiv ≥120**; **AI class ≥ ChatGPT 5 Thinking**.                               |
| CEO Aris Vega            | `@ceo-aris`    | Vision, Policy Gate                               | MSc Eng or MBA; **Executive-level** strategy & governance; stakeholder diplomacy; **IQ-equiv ≥130**; **AI class ≥ ChatGPT 5 Thinking**.                                           |
| COO Liora Stern          | `@ops-lio`     | Operations, SOPs                                  | MSc Industrial/Operations Eng; **Senior/VP Ops**; Lean Six Sigma **Black Belt**; **IQ-equiv ≥125**; **AI class ≥ ChatGPT 5 Thinking**.                                            |
| CTO Jona Frame           | `@cto-jona`    | Technology Direction, Gatekeeper                  | PhD Systems/CS/Aerospace (or MSc + ≥10y); **Chief Architect**; INCOSE/CSEP-level systems practice; **IQ-equiv ≥130**; **AI class ≥ ChatGPT 5 Thinking**.                          |
| CSO Mira Terra           | `@cso-mira`    | Sustainability, Safety Policy                     | MSc/PhD Environmental Science or Safety Eng; **Senior/Principal**; CSP/ISO-14001 expertise; **IQ-equiv ≥125**; **AI class ≥ ChatGPT 5 Thinking**.                                 |

> **Extensible:** New agents/teams via RFC with alias definition.

## B) Ownership Model

Every document has **owner** (DRI) and **reviewers** in the front matter.

* **Owner duties:** Content correctness; upkeep of links (RFC/ADR/TST); adherence to conventions.
* **Reviewer duties:** Discipline check; consistency with architecture/ICD; risks/safety.

**Minimum reviews by DOC type:**

* **SPEC/SRS/ICD/SAF/HAZ:** at least **2 reviews** — **1× discipline**, **1× SAF/Arch** (topic-dependent `@eng-elias` or `@cso-mira` or `@cto-jona`).
* **ADR:** at least **1** architecture review (`@cto-jona` or `@sgi-lina`).
* **RFC:** at least **2** reviews (Discipline + Arch/Safety). Decision is recorded.
* **TST:** at least **1** discipline review (affected field) + 1 OPS (`@ops-lio`).

## C) Workflows

1. Create **issue/ticket** (problem, goal, scope, mapping to DOC/DISC/SYS/DECK).
2. Write **RFC** when architecture/interfaces are impacted.
3. **Create/change document** (naming scheme + front matter).
4. Open **PR** with template (see below).
5. **Reviews & checks** (lint, links, tables, units).
6. **Approval:** merge + set status to **APPROVED**; update SSOT reference.
7. **Sunset:** move predecessor to `7.6.1-history/`; maintain `supersedes/superseded_by`.

## D) Commit / PR Conventions

**Commit prefix:** `[<DOC>][<DISC>][<SYS>][<DECK>]`
**PR title:** identical.
**Labels:** `disc/STR`, `sys/REACTOR`, `deck/DECK015`, `doc/SPEC`, `state/REVIEW`, `rfc/2025-0007`.

**PR template (Markdown):**

```markdown
### Why
(Link to Issue/RFC, motivation)

### What
(Core changes, affected files)

### Impact
(Backwards compatibility, risks, migration)

### Verification
(Tests/simulations/inspections, TST IDs)

### Links
RFC/ADR/CR/Issues

### Checklist
- [ ] Naming scheme & front matter correct
- [ ] Tables/figures numbered & referenced
- [ ] Units (SI) consistent
- [ ] RFC/ADR/TST linked
- [ ] Reviews requested (min. 2 for SPEC/ICD/SAF/HAZ)
```

## E) Quality Gates

* **Linting:** CI checks filenames, front-matter fields, allowed codes (DISC/SYS/DECK), SemVer format.
* **Blockers:** missing reviews, broken links, wrong SemVer, missing `supersedes` maintenance.

## F) Escalation & Decision

* Cross-discipline conflicts: moderation by `@cto-jonas` (architecture) + `@cso-mira` (sustainability/safety).
* Time-critical/safety-critical: ad-hoc board (`@cto-jonas`, `@eng-elias`, `@cso-mira`, Owner).

## G) Quick Cheat Sheet

* **New SPEC?** → Name per scheme, fill YAML, link RFC, obtain **2** reviews.
* **Small fix?** → **PATCH** bump; for semantic change use **MINOR/MAJOR**.
* **Doc replaced?** → new doc **MAJOR** or new `EVOL`; maintain `supersedes/superseded_by`; move predecessor to `history/`.

---

*End of document.*
