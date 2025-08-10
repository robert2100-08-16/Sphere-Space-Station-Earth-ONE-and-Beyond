# AGENTS.md (Arbeitsanweisungen & Verantwortlichkeiten)

> Dieses Kapitel kann 1:1 als `AGENTS.md` in das Repository übernommen werden.

## A) Agenten & Kurz‑Aliasse

| Rolle / Name             | Alias          | Schwerpunkt                                      |
| ------------------------ | -------------- | ------------------------------------------------ |
| Engineer SGI Lina        | `@sgi-lina`    | Struktur & Integration (STR, ARCH)               |
| Engineer Leo             | `@eng-leo`     | Feldtests, Kundenlösungen (OPS, TST)             |
| Engineer Kai Nova        | `@eng-kai`     | Antrieb & Habitat (PROP, STR)                    |
| Engineer Mara Flux       | `@eng-mara`    | Energie & Ressourcenflüsse (PWR, THM)            |
| Engineer Elias Core      | `@eng-elias`   | Kernsysteme, Reaktor, Safety‑Arch (REACTOR, SAF) |
| Economist Alethea Voss   | `@eco-alethea` | Markt/Trends (impact‑review)                     |
| Economist Orion Hale     | `@eco-orion`   | Invest (impact‑review)                           |
| CFO Terra Chen           | `@cfo-terra`   | Kosten, CAPEX/OPEX                               |
| Trade Analyst Nova Reyes | `@trade-nova`  | Transport/Rohstoffe                              |
| CEO Aris Vega            | `@ceo-aris`    | Vision, Policy‑Gate                              |
| COO Liora Stern          | `@ops-lio`     | Betrieb, SOPs                                    |
| CTO Jonas Frame          | `@cto-jonas`   | Technische Richtung, Gatekeeper                  |
| CSO Mira Terra           | `@cso-mira`    | Nachhaltigkeit, Safety‑Policy                    |

> **Erweiterbar:** Neue Agenten/Teams via RFC mit Alias‑Def.

## B) Ownership‑Modell

Jedes Dokument hat **owner** (DRI) und **reviewers** im Front‑Matter.

* **Owner‑Pflichten:** Inhaltliche Korrektheit, Pflege von Links (RFC/ADR/TST), Einhaltung der Konvention.
* **Reviewer‑Pflichten:** Fachprüfung (Disziplin), Konsistenz zu Architektur/ICD, Risiken/Safety.

**Minimal‑Reviews pro DOC‑Typ:**

* **SPEC/SRS/ICD/SAF/HAZ:** mind. 2 Reviews – davon **1× fachlich**, **1× SAF/Arch** (je nach Thema `@eng-elias` oder `@cso-mira` bzw. `@cto-jonas`).
* **ADR:** mind. 1 Arch‑Review (`@cto-jonas` oder `@sgi-lina`).
* **RFC:** mind. 2 Reviews (Fach + Arch/Safety). Entscheid wird protokolliert.
* **TST:** mind. 1 Fach‑Review (betroffene Disziplin) + 1 OPS (`@ops-lio`).

## C) Arbeitsabläufe

1. **Issue/Ticket** anlegen (Problem, Ziel, Scope, Zugehörigkeit DOC/DISC/SYS/DECK).
2. **RFC** schreiben, wenn Architektur/Schnittstellen betroffen sind.
3. **Dokument anlegen/ändern** (Namensschema + Front‑Matter).
4. **PR erstellen** mit Template (siehe unten).
5. **Reviews & Checks** (Lint, Links, Tabellen, Einheiten).
6. **Freigabe:** Merge + Statuswechsel auf **APPROVED**; SSOT‑Verweis aktualisieren.
7. **Ablösung:** Vorgänger nach `7.6.1-history/` verschieben; `supersedes/superseded_by` pflegen.

## D) Commit‑/PR‑Konventionen

**Commit‑Prefix:** `[<DOC>][<DISC>][<SYS>][<DECK>]`
**PR‑Titel:** identisch.
**Labels:** `disc/STR`, `sys/REACTOR`, `deck/DECK015`, `doc/SPEC`, `state/REVIEW`, `rfc/2025-0007`.

**PR‑Template (Markdown):**

```markdown
### Why
(Bezug zum Issue/RFC, Motivation)

### What
(Kernänderungen, betroffene Dateien)

### Impact
(Backwards Compatibility, Risiken, Migration)

### Verification
(Tests/Simulationen/Prüfungen, Verweise TST‑IDs)

### Links
RFC/ADR/CR/Issues

### Checklist
- [ ] Namensschema & Front‑Matter korrekt
- [ ] Tabellen/Abbildungen nummeriert & referenziert
- [ ] Einheiten (SI) konsistent
- [ ] RFC/ADR/TST verlinkt
- [ ] Reviews angefragt (min. 2 bei SPEC/ICD/SAF/HAZ)
```

## E) Quality Gates

* **Linting:** CI prüft Dateinamen, Front‑Matter‑Felder, erlaubte Codes (DISC/SYS/DECK), SemVer‑Format.
* **Blocker:** fehlende Reviews, kaputte Links, falsches SemVer, fehlende `supersedes`‑Pflege.

## F) Eskalation & Entscheid

* Konflikte zwischen Disziplinen: Moderation durch `@cto-jonas` (Architektur) + `@cso-mira` (Nachhaltigkeit/Safety).
* Zeitkritisch/sicherheitskritisch: Ad‑hoc‑Board (`@cto-jonas`, `@eng-elias`, `@cso-mira`, Owner).

## G) Kurz‑Cheatsheet

* **Neues SPEC?** → Dateiname nach Schema, YAML füllen, RFC verlinken, 2 Reviews einholen.
* **Kleine Korrektur?** → PATCH‑Bump; bei Bedeutungsänderung MINOR/MAJOR.
* **Doc ersetzt?** → neues Doc **MAJOR** oder neue `EVOL`, `supersedes`/`superseded_by` pflegen, Vorgänger in `history/`.

---

*Ende des Dokuments.*