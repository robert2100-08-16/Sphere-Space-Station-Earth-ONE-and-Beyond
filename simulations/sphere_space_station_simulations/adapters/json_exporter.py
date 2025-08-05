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

from ..data_model import (
    BaseRing,
    Deck,
    Hull,
    Material,
    StationModel,
    Window,
    Wormhole,
)


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


def import_json(filepath: str | Path) -> StationModel:
    """Load a :class:`StationModel` from a JSON file."""

    def _mat(data: dict | None) -> Material | None:
        return Material(**data) if data else None

    def _window(data: dict) -> Window:
        return Window(
            position=tuple(data["position"]),
            size_m=data["size_m"],
            count=data.get("count", 1),
            material=_mat(data.get("material")),
        )

    path = Path(filepath)
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    decks = []
    for d in data.get("decks", []):
        decks.append(
            Deck(
                id=d["id"],
                inner_radius_m=d["inner_radius_m"],
                outer_radius_m=d["outer_radius_m"],
                height_m=d["height_m"],
                windows=[_window(w) for w in d.get("windows", [])],
                net_inner_radius_m=d.get("net_inner_radius_m"),
                net_outer_radius_m=d.get("net_outer_radius_m"),
                net_height_m=d.get("net_height_m"),
                base_area_m2=d.get("base_area_m2"),
                volume_m3=d.get("volume_m3"),
                material=_mat(d.get("material")),
            )
        )

    base_rings = []
    for r in data.get("base_rings", []):
        base_rings.append(
            BaseRing(
                radius_m=r["radius_m"],
                width_m=r["width_m"],
                position_z_m=r["position_z_m"],
                material=_mat(r.get("material")),
            )
        )

    hull_obj = None
    hull = data.get("hull")
    if hull:
        hull_obj = Hull(
            radius_m=hull["radius_m"],
            windows=[_window(w) for w in hull.get("windows", [])],
            net_radius_m=hull.get("net_radius_m"),
            surface_area_m2=hull.get("surface_area_m2"),
            volume_m3=hull.get("volume_m3"),
            material=_mat(hull.get("material")),
        )

    worm_obj = None
    worm = data.get("wormhole")
    if worm:
        worm_obj = Wormhole(
            radius_m=worm["radius_m"],
            height_m=worm["height_m"],
            base_thickness_m=worm.get("base_thickness_m", 0.0),
            material=_mat(worm.get("material")),
        )

    return StationModel(
        decks=decks, base_rings=base_rings, hull=hull_obj, wormhole=worm_obj
    )
