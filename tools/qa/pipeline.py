"""Quality assurance processing pipeline.

This module orchestrates the QA workflow consisting of:
1. Import
2. Pre-Check
3. Semantic Analysis
4. Safety Simulation
5. Issue Tagging
6. Report Creation
7. Review
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .checklist import CHECKLISTS, check_completeness
from .consistency import find_contradictions
from .factual_accuracy import check_factual_accuracy
from .history import record_release
from .presentation import generate_pitch
from .safety import simulate_safety_scenarios
from .traceability import link_sources


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------

def import_document(data_or_path: Any) -> dict:
    """Import a document from a mapping or JSON file."""
    if isinstance(data_or_path, (str, Path)):
        with open(data_or_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return data_or_path


def pre_check(document: dict, template: str = "technical_report") -> dict:
    """Check document completeness against a checklist template."""
    checklist = CHECKLISTS.get(template, {})
    return check_completeness(document, checklist)


def semantic_analysis(document: dict) -> dict:
    """Placeholder for semantic analysis step."""
    return {"semantics": document.get("text", "")}


def safety_simulation(document: dict) -> dict:
    """Run safety scenario simulations on the document."""
    return simulate_safety_scenarios(document.get("text", ""))


def tag_issues(pre: dict, safety: dict) -> list[dict[str, str]]:
    """Combine pre-check and safety results into tagged issues."""
    issues: list[dict[str, str]] = []
    for section, items in pre.items():
        for item in items:
            issues.append(
                {
                    "category": "pre_check",
                    "reference": item,
                    "description": f"missing {section[:-1]}",
                }
            )
    for scenario, problems in safety.items():
        issues.append(
            {
                "category": "safety",
                "reference": scenario,
                "description": ", ".join(problems),
            }
        )
    return issues


def create_report(issues: list[dict[str, str]], output_dir: Path | None = None) -> Path:
    """Write a QA report with chapter references and categorization."""
    output_dir = (
        output_dir
        or Path(__file__).resolve().parent.parent / "reports" / "qa"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    report_path = output_dir / f"qa-report-{timestamp}.md"
    lines = ["# QA Report", ""]
    for issue in issues:
        lines.append(
            f"- [{issue['category']}] {issue['reference']}: {issue['description']}"
        )
    with report_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return report_path


def review(report_path: Path) -> str:
    """Return a review message for the generated report."""
    return f"Report stored at {report_path}"


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------

def run_pipeline(
    document: Any,
    presentation_format: str | None = None,
    template: str = "technical_report",
) -> dict:
    """Run QA pipeline on a document."""
    doc = import_document(document)

    # Pre-existing QA checks
    check_factual_accuracy(doc)
    doc["source_links"] = link_sources(doc)

    chapters = doc.get("chapters") or []
    for i, chapter_a in enumerate(chapters):
        for chapter_b in chapters[i + 1 :]:
            find_contradictions(chapter_a, chapter_b)

    # New pipeline steps
    pre = pre_check(doc, template)
    semantic = semantic_analysis(doc)
    safety = safety_simulation(doc)
    issues = tag_issues(pre, safety)
    report_path = create_report(issues)
    review_message = review(report_path)
    history_path = record_release(report_path, f"{len(issues)} issues")

    result = {
        "pre_check": pre,
        "semantic": semantic,
        "safety": safety,
        "issues": issues,
        "report_path": str(report_path),
        "review": review_message,
        "history": str(history_path),
    }

    if presentation_format == "pitch":
        result["pitch"] = generate_pitch(doc, doc.get("audience", "general"))

    return result
