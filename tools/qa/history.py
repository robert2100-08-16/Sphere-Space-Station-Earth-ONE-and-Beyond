"""Utilities to record QA release history."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import shutil

HISTORY_DIR = (
    Path(__file__).resolve().parent.parent / "reports" / "qa" / "history"
)
HISTORY_FILE = HISTORY_DIR / "history.json"


def record_release(report_path: Path, result: str) -> Path:
    """Store a QA release entry with timestamp and result.

    Parameters
    ----------
    report_path:
        Path to the generated QA report.
    result:
        Summary of the QA outcome (e.g., "pass", "fail").
    """
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = HISTORY_DIR / Path(report_path).name
    shutil.copy(report_path, archive_path)
    entry = {
        "date": datetime.utcnow().isoformat(timespec="seconds"),
        "report": str(archive_path),
        "result": result,
    }
    data: List[Dict[str, str]] = []
    if HISTORY_FILE.exists():
        try:
            data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = []
    data.append(entry)
    HISTORY_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return HISTORY_FILE
