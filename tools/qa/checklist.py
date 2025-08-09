"""Checklists for mandatory sections and completeness checks."""

# Required sections for each document type
CHECKLISTS = {
    "technical_report": {
        "chapters": [
            "Introduction",
            "System Overview",
            "Testing",
            "Conclusion",
        ],
        "tables": [
            "Requirements",
            "Results",
        ],
    },
    "financial_report": {
        "chapters": [
            "Executive Summary",
            "Financial Overview",
            "Risk Assessment",
        ],
        "tables": [
            "Budget",
            "ROI",
        ],
    },
}


def check_completeness(document, template):
    """Return missing sections compared to template.

    Parameters
    ----------
    document : dict
        Mapping with keys like ``chapters`` and ``tables`` listing the
        sections present in the document.
    template : dict
        Checklist dictionary with required sections for the document type.

    Returns
    -------
    dict
        Keys map to lists of missing entries. An empty dict means no missing
        sections were detected.
    """
    missing = {}

    for key in template:
        required_list = template.get(key, [])
        present = set(document.get(key, []))
        absent = [item for item in required_list if item not in present]
        if absent:
            missing[key] = absent

    return missing
