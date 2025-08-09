"""Processing pipeline for QA tasks."""

from .factual_accuracy import check_factual_accuracy
from .consistency import find_contradictions
from .traceability import link_sources
from .presentation import generate_pitch


def semantic_analysis(document):
    """Placeholder for semantic analysis step."""
    return {"semantics": document.get("text", "")}


def run_pipeline(document, presentation_format: str | None = None):
    """Run QA pipeline on a document.

    Parameters
    ----------
    document:
        Mapping representing the document.
    presentation_format:
        If set to ``"pitch"`` an additional ``"pitch"`` entry is attached to
        the returned data containing a bullet-point version of ``document``.
    """
    check_factual_accuracy(document)

    # Link chapters to external sources and verify references
    document["source_links"] = link_sources(document)

    # Consistency checks across chapters
    chapters = document.get("chapters") or []
    for i, chapter_a in enumerate(chapters):
        for chapter_b in chapters[i + 1 :]:
            find_contradictions(chapter_a, chapter_b)

    # Semantic Analysis
    result = semantic_analysis(document)

    if presentation_format == "pitch":
        result["pitch"] = generate_pitch(document, document.get("audience", "general"))

    return result
