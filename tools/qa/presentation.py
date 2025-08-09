"""Utilities for presenting documents to different audiences.

This module provides terminology checking and readability analysis
as well as helpers to validate a short "pitch" representation of a
text.  The functions are intentionally simple – they perform lightweight
heuristics that are sufficient for unit testing and illustrative use
within the QA pipeline.
"""

from __future__ import annotations

import re
from typing import Iterable, Dict, List


def check_terminology(text: str, allowed_terms: Iterable[str]) -> bool:
    """Ensure that ``text`` only uses words from ``allowed_terms``.

    Parameters
    ----------
    text:
        The text to validate.
    allowed_terms:
        Iterable of permitted terms.  The comparison is case-insensitive.

    Returns
    -------
    bool
        ``True`` if all words are contained in ``allowed_terms``.

    Raises
    ------
    ValueError
        If unknown terminology is encountered.  The error message lists the
        offending terms.
    """

    words = re.findall(r"\b\w+\b", text.lower())
    allowed = {t.lower() for t in allowed_terms}
    unknown = sorted(set(w for w in words if allowed and w not in allowed))

    if unknown:
        raise ValueError(f"Unknown terminology: {', '.join(unknown)}")

    return True


def analyze_readability(text: str, audience: str) -> Dict[str, float]:
    """Assess readability of ``text`` for the given ``audience``.

    The analysis is based on the average sentence length in words and a
    simple threshold for each audience type.  If the text exceeds the
    threshold for the audience, a :class:`ValueError` is raised.

    Parameters
    ----------
    text:
        Text to analyse.
    audience:
        One of ``"kids"``, ``"general"`` or ``"experts"``.  Unknown
        audiences default to the ``"general"`` threshold.

    Returns
    -------
    dict
        Dictionary with ``avg_sentence_length`` and ``threshold``.

    Raises
    ------
    ValueError
        If the text is considered too difficult for the audience.
    """

    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]
    word_counts = [len(s.split()) for s in sentences]
    avg_length = sum(word_counts) / len(word_counts) if word_counts else 0.0

    thresholds = {"kids": 10, "general": 20, "experts": 40}
    threshold = thresholds.get(audience, thresholds["general"])

    if avg_length > threshold:
        raise ValueError(
            f"Text too complex for {audience}: avg sentence length {avg_length:.1f} > {threshold}"
        )

    return {"avg_sentence_length": avg_length, "threshold": threshold}


def validate_pitch(pitch: str) -> bool:
    """Validate formatting and tone of a pitch.

    The pitch must consist of bullet points, each starting with ``"- "``.
    Additionally, the text must not contain negative vocabulary such as
    ``"bad"`` or ``"hate"`` which would indicate an unsuitable tone for a
    promotional pitch.

    Returns
    -------
    bool
        ``True`` if the pitch passes validation.

    Raises
    ------
    ValueError
        If formatting or tone issues are detected.
    """

    lines = [line for line in pitch.splitlines() if line.strip()]
    if not all(line.startswith("- ") for line in lines):
        raise ValueError("Pitch must be formatted with '- ' bullet points")

    negative_words = {"bad", "hate", "awful", "ugly"}
    words = re.findall(r"\b\w+\b", pitch.lower())
    if any(word in negative_words for word in words):
        raise ValueError("Pitch contains unsuitable tone")

    return True


def generate_pitch(document: Dict[str, str], audience: str = "general", allowed_terms: Iterable[str] | None = None) -> str:
    """Generate a bullet-point pitch from ``document``.

    Parameters
    ----------
    document:
        Mapping with a ``"text"`` key containing the source text.
    audience:
        Target audience for readability checks.
    allowed_terms:
        Optional iterable of allowed terminology.  If provided, the pitch is
        checked against this list.

    Returns
    -------
    str
        The formatted pitch text.

    Raises
    ------
    ValueError
        If terminology, readability or pitch validation fails.
    """

    text = document.get("text", "")
    pitch = "\n".join(f"- {line.strip()}" for line in text.splitlines() if line.strip())

    if allowed_terms is not None:
        check_terminology(pitch, allowed_terms)

    analyze_readability(pitch, audience)
    validate_pitch(pitch)

    return pitch
