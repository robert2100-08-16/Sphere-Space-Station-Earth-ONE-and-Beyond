"""Prototype glTF exporter.

Creates a trivial glTF 2.0 file containing metadata about decks and hull.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..data_model import StationModel


def export_gltf(model: StationModel, filepath: str | Path) -> Path:
    """Write a minimal glTF file with station metadata."""

    path = Path(filepath)
    data = {
        "asset": {"version": "2.0"},
        "extras": {
            "deck_count": len(model.decks),
            "has_hull": model.hull is not None,
        },
    }
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh)
    return path
