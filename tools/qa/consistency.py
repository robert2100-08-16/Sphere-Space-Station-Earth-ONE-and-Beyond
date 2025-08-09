"""Consistency checking utilities for QA pipeline."""


def _normalize_key(key):
    """Normalize keys for semantic comparison.

    Converts keys to lowercase and replaces spaces or hyphens with underscores
    so that semantically equivalent keys can be matched.
    """
    return key.lower().replace("-", "_").replace(" ", "_")


def _normalize_document(doc):
    """Return a new dict with normalized keys for comparison."""
    return {_normalize_key(k): v for k, v in doc.items()}


def find_contradictions(doc_a, doc_b):
    """Check for contradictory values between two documents.

    Parameters
    ----------
    doc_a, doc_b : dict
        Mappings of metric names to values. Keys are normalized in a
        case-insensitive manner to support simple semantic comparisons.

    Returns
    -------
    bool
        ``True`` if no contradictions are found.

    Raises
    ------
    ValueError
        If conflicting values are detected for any shared keys.
    """
    normalized_a = _normalize_document(doc_a)
    normalized_b = _normalize_document(doc_b)

    contradictions = []

    for key in normalized_a.keys() & normalized_b.keys():
        if normalized_a[key] != normalized_b[key]:
            contradictions.append(f"{key}: {normalized_a[key]} vs {normalized_b[key]}")

    if contradictions:
        raise ValueError("Contradictions found: " + "; ".join(contradictions))

    return True
