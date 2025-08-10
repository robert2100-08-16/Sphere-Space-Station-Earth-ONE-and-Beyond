import pytest

from tools.qa.presentation import validate_pitch, check_terminology, analyze_readability
from tools.qa.pipeline import run_pipeline


def test_validate_pitch_detects_formatting_issue():
    bad_pitch = "Intro line without bullet\n- Proper bullet"
    with pytest.raises(ValueError):
        validate_pitch(bad_pitch)


def test_validate_pitch_detects_bad_tone():
    bad_pitch = "- This product is bad and we hate its limits"
    with pytest.raises(ValueError):
        validate_pitch(bad_pitch)


def test_pipeline_generates_pitch_format():
    document = {"text": "Point one\nPoint two", "audience": "general"}
    result = run_pipeline(document, presentation_format="pitch")
    assert result["pitch"].splitlines()[0].startswith("- ")
    assert result["pitch"].splitlines()[1].startswith("- ")


def test_terminology_and_readability_checks():
    text = "Point one\nPoint two"
    # Terminology check passes when all words are allowed
    assert check_terminology(text, {"point", "one", "two"}) is True
    # Readability check fails for kids audience if sentences are long
    long_text = "This sentence is excessively long for young readers and therefore problematic."
    with pytest.raises(ValueError):
        analyze_readability(long_text, "kids")
