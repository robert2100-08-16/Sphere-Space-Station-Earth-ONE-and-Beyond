import pytest

from tools.qa.factual_accuracy import check_factual_accuracy


def test_passes_with_correct_metrics():
    doc = {"max_load": 1000, "min_temp": -50}
    assert check_factual_accuracy(doc) is True


def test_detects_incorrect_max_load():
    doc = {"max_load": 900, "min_temp": -50}
    with pytest.raises(ValueError):
        check_factual_accuracy(doc)


def test_detects_incorrect_min_temp():
    doc = {"max_load": 1000, "min_temp": -40}
    with pytest.raises(ValueError):
        check_factual_accuracy(doc)
