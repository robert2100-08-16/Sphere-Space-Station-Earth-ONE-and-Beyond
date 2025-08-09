"""Utilities for linking document sections with external sources."""


def link_sources(document):
    """Link chapter numbers to external source identifiers.

    Parameters
    ----------
    document : dict
        Mapping describing the document. Expected keys are ``chapters`` and
        ``external_sources``. Each chapter must provide a ``number`` and may
        list referenced source identifiers in ``sources``.

    Returns
    -------
    dict
        Mapping of chapter numbers to lists of external source identifiers.

    Raises
    ------
    ValueError
        If any external source is not referenced by at least one chapter.
    """
    chapters = document.get("chapters", [])
    external_sources = set(document.get("external_sources", []))

    source_map = {}
    referenced = set()

    for chapter in chapters:
        number = chapter.get("number")
        if number is None:
            raise ValueError("Chapter missing 'number'")
        sources = chapter.get("sources", [])
        source_map[number] = sources
        referenced.update(sources)

    missing = sorted(external_sources - referenced)
    if missing:
        raise ValueError(
            "Unreferenced external sources: " + ", ".join(missing)
        )

    return source_map
