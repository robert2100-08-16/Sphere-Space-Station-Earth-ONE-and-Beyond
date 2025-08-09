import pytest

from tools.qa.consistency import find_contradictions
from tools.qa.pipeline import run_pipeline


def test_no_contradictions():
    doc_a = {"max_load": 1000, "min_temp": -50}
    doc_b = {"max_load": 1000, "min_temp": -50}
    assert find_contradictions(doc_a, doc_b) is True


def test_detects_contradictions():
    doc_a = {"max_load": 1000, "min_temp": -50}
    doc_b = {"max_load": 900, "min_temp": -50}
    with pytest.raises(ValueError):
        find_contradictions(doc_a, doc_b)


def test_pipeline_detects_chapter_contradictions():
    document = {
        "max_load": 1000,
        "min_temp": -50,
        "chapters": [
            {"max_load": 1000, "min_temp": -50},
            {"max_load": 900, "min_temp": -50},
        ],
    }
    with pytest.raises(ValueError):
        run_pipeline(document)
