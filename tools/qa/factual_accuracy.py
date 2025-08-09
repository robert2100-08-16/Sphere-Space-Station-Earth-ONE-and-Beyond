"""Factual accuracy verification utilities."""

# Internal reference data (Section 8.4.2)
INTERNAL_REFERENCE = {
    "max_load": 1000,
    "min_temp": -50,
}

# External standards from agencies
EXTERNAL_STANDARDS = {
    "ISO": {"max_load": 1000},
    "NASA": {"min_temp": -50},
    "ESA": {"max_load": 1000, "min_temp": -50},
}


def check_factual_accuracy(document):
    """Compare document metrics to internal and external references.

    Parameters
    ----------
    document : dict
        Mapping of metric names to values extracted from a document.

    Raises
    ------
    ValueError
        If any metric differs from internal reference data or external standards.
    """
    discrepancies = []

    for metric, expected in INTERNAL_REFERENCE.items():
        value = document.get(metric)
        if value is not None and value != expected:
            discrepancies.append(
                f"{metric}: expected {expected} (internal) but got {value}"
            )

    for agency, standards in EXTERNAL_STANDARDS.items():
        for metric, expected in standards.items():
            value = document.get(metric)
            if value is not None and value != expected:
                discrepancies.append(
                    f"{metric}: expected {expected} ({agency}) but got {value}"
                )

    if discrepancies:
        raise ValueError("Factual discrepancies found: " + "; ".join(discrepancies))

    return True
