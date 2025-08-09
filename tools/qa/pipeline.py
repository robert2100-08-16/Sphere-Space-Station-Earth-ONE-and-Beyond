"""Processing pipeline for QA tasks."""

from .factual_accuracy import check_factual_accuracy
from .consistency import find_contradictions
from .traceability import link_sources


def semantic_analysis(document):
    """Placeholder for semantic analysis step."""
    return {"semantics": document.get("text", "")}


def run_pipeline(document):
    """Run QA pipeline on a document."""
    check_factual_accuracy(document)

    # Link chapters to external sources and verify references
    document["source_links"] = link_sources(document)

    # Consistency checks across chapters
    chapters = document.get("chapters") or []
    for i, chapter_a in enumerate(chapters):
        for chapter_b in chapters[i + 1 :]:
            find_contradictions(chapter_a, chapter_b)

    # Semantic Analysis
    return semantic_analysis(document)
