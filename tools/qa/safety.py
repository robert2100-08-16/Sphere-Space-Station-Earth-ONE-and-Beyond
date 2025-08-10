"""Safety scenario simulation utilities."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

# ---------------------------------------------------------------------------
# logging configuration
# ---------------------------------------------------------------------------

LOG_DIR = Path(__file__).resolve().parents[2] / "logs" / "safety"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "audit.log"

logger = logging.getLogger("safety_audit")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


SCENARIOS = {
    "fire": ["fire"],
    "radiation": ["radiation"],
    "pressure_loss": ["pressure loss", "decompression"],
}


def check_technical_protection(text: str) -> List[str]:
    """Verify presence of core technical protection systems.

    The heuristic ensures that the document mentions basic suppression,
    shielding and pressure relief systems.  Missing items are returned as a
    list of issue descriptions.
    """

    issues: List[str] = []
    if "fire suppression" not in text and "sprinkler" not in text:
        issues.append("missing fire suppression system")
    if "radiation shielding" not in text:
        issues.append("missing radiation shielding")
    if "pressure valve" not in text and "pressure relief" not in text:
        issues.append("missing pressure relief")

    if issues:
        logger.info("Technical protection issues: %s", "; ".join(issues))
    else:
        logger.info("Technical protection check passed")

    return issues


def check_evacuation_logistics(text: str) -> List[str]:
    """Assess evacuation planning and logistics in ``text``."""

    issues: List[str] = []
    if "evacuation route" not in text:
        issues.append("missing evacuation route")
    if "assembly point" not in text:
        issues.append("missing assembly point")
    if "drill schedule" not in text and "evacuation drill" not in text:
        issues.append("missing drill schedule")

    if issues:
        logger.info("Evacuation logistics issues: %s", "; ".join(issues))
    else:
        logger.info("Evacuation logistics check passed")

    return issues


def check_redundancies(text: str) -> List[str]:
    """Ensure redundant systems are documented."""

    issues: List[str] = []
    if "redundant system" not in text:
        issues.append("missing redundant system")
    if "backup power" not in text:
        issues.append("missing backup power")
    if "failover" not in text:
        issues.append("missing failover plan")

    if issues:
        logger.info("Redundancy issues: %s", "; ".join(issues))
    else:
        logger.info("Redundancy check passed")

    return issues


def simulate_safety_scenarios(document: str) -> Dict[str, List[str]]:
    """Check emergency preparedness for fire, radiation and pressure loss.

    Parameters
    ----------
    document : str
        Text describing safety procedures.

    Returns
    -------
    dict
        Mapping of scenario names to lists of detected issues. An empty
        dictionary indicates no problems were found.
    """

    text = document.lower()
    results: Dict[str, List[str]] = {}

    for name, keywords in SCENARIOS.items():
        issues: List[str] = []
        if not any(k in text for k in keywords):
            issues.append("scenario not addressed")

        issues.extend(check_technical_protection(text))
        issues.extend(check_evacuation_logistics(text))
        issues.extend(check_redundancies(text))

        if issues:
            results[name] = issues

    logger.info("Simulation results: %s", results or "no issues")
    return results
