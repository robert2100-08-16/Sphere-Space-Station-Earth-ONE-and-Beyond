"""Prototype STEP exporter.

Writes a very small placeholder STEP file describing decks and hull radius.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from ..data_model import Hull, StationModel

HEADER = "ISO-10303-21;\nHEADER;\nENDSEC;\nDATA;\n"
FOOTER = "ENDSEC;\nEND-ISO-10303-21;\n"


def _iter_lines(model: StationModel) -> Iterable[str]:
    for deck in model.decks:
        yield f"/* deck {deck.id} */\n"
    if model.hull:
        yield f"/* hull radius {model.hull.radius_m} */\n"


def export_step(model: StationModel, filepath: str | Path) -> Path:
    """Write a minimal STEP file.

    Parameters
    ----------
    model: StationModel
        Geometry to export.
    filepath: str | Path
        Output filename.
    """

    path = Path(filepath)
    with path.open("w", encoding="utf-8") as fh:
        fh.write(HEADER)
        for line in _iter_lines(model):
            fh.write(line)
        fh.write(FOOTER)
    return path
