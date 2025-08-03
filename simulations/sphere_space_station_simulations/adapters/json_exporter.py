"""Simple JSON exporter for :class:`StationModel`.

The exporter serialises the complete data model into a human readable
JSON file.  It relies on :func:`dataclasses.asdict` which correctly
handles nested dataclasses such as decks with windows or hull
specifications.  Tuples are converted to lists to remain valid JSON.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ..data_model import StationModel


def export_json(model: StationModel, filepath: str | Path) -> Path:
    """Export the station model to a JSON file.

    Parameters
    ----------
    model:
        The :class:`StationModel` instance to serialise.
    filepath:
        Destination path for the generated JSON document.

    Returns
    -------
    Path
        The path to the written file.
    """

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(asdict(model), handle, indent=2)
    return path
