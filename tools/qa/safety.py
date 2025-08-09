"""Safety scenario simulation utilities."""

SCENARIOS = {
    "fire": ["fire"],
    "radiation": ["radiation"],
    "pressure_loss": ["pressure loss", "decompression"],
}


def simulate_safety_scenarios(document):
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
    results = {}

    for name, keywords in SCENARIOS.items():
        issues = []
        if not any(k in text for k in keywords):
            issues.append("scenario not addressed")
        if "evacuation route" not in text:
            issues.append("missing evacuation route")
        if "redundant system" not in text:
            issues.append("missing redundant system")
        if issues:
            results[name] = issues

    return results
