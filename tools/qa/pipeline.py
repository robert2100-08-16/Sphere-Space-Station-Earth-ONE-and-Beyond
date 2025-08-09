"""Processing pipeline for QA tasks."""

from .factual_accuracy import check_factual_accuracy


def semantic_analysis(document):
    """Placeholder for semantic analysis step."""
    return {"semantics": document.get("text", "")}


def run_pipeline(document):
    """Run QA pipeline on a document."""
    check_factual_accuracy(document)
    # Semantic Analysis
    return semantic_analysis(document)
