"""QA status dashboard utilities.

Provides an overview of open findings from the latest QA report
and derives a simple document maturity state based on the number
of unresolved issues.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports" / "qa"


def _parse_issues(report_path: Path) -> List[Dict[str, str]]:
    """Extract issue entries from a QA report."""
    issues: List[Dict[str, str]] = []
    with report_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line.startswith("- [") and ":" in line:
                category = line.split("[", 1)[1].split("]", 1)[0]
                ref_desc = line.split("]", 1)[1].strip()
                reference, description = (part.strip() for part in ref_desc.split(":", 1))
                issues.append({
                    "category": category,
                    "reference": reference,
                    "description": description,
                })
    return issues


def load_latest_findings() -> List[Dict[str, str]]:
    """Return issues from the most recent QA report, if any."""
    reports = sorted(REPORTS_DIR.glob("qa-report-*.md"))
    if not reports:
        return []
    return _parse_issues(reports[-1])


def document_maturity(open_issues: int) -> str:
    """Derive a simple maturity level based on number of open issues."""
    if open_issues == 0:
        return "release"
    if open_issues < 5:
        return "review"
    return "draft"


def dashboard_summary() -> Dict[str, object]:
    """Return dashboard data with findings and maturity level."""
    findings = load_latest_findings()
    return {
        "open_findings": findings,
        "maturity": document_maturity(len(findings)),
    }


if __name__ == "__main__":  # pragma: no cover - manual execution helper
    import json

    print(json.dumps(dashboard_summary(), indent=2))
