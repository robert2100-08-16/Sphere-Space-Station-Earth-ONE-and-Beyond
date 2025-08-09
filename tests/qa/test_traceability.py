import pytest

from tools.qa.traceability import link_sources
from tools.qa.pipeline import run_pipeline


def test_links_chapter_sources():
    document = {
        "chapters": [
            {"number": "1", "sources": ["ISO"]},
            {"number": "2", "sources": ["NASA"]},
        ],
        "external_sources": ["ISO", "NASA"],
    }
    mapping = link_sources(document)
    assert mapping == {"1": ["ISO"], "2": ["NASA"]}


def test_detects_unreferenced_source():
    document = {
        "chapters": [{"number": "1", "sources": ["ISO"]}],
        "external_sources": ["ISO", "NASA"],
    }
    with pytest.raises(ValueError):
        link_sources(document)


def test_pipeline_flags_unreferenced_source():
    document = {
        "chapters": [{"number": "1", "sources": ["ISO"]}],
        "external_sources": ["ISO", "NASA"],
    }
    with pytest.raises(ValueError):
        run_pipeline(document)
