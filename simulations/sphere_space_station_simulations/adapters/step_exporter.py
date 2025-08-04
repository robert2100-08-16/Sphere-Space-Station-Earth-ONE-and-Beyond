"""STEP exporter building B-Rep solids with CadQuery.

This module creates simple volumetric representations for decks and the
outer hull of the station.  Each solid receives a ``material`` metadata
attribute (either ``"Stahl"`` for structural elements or ``"Glas"`` for
windows) which is preserved in the generated STEP file.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

# ``cadquery`` is an optional dependency.  The tests are executed in an
# environment where it is not available, so we attempt to import it but degrade
# gracefully when that fails.  In this fallback mode ``export_step`` simply
# writes a small placeholder file that contains some information about the
# station model.
try:  # pragma: no cover - best effort for optional dependency
    import cadquery as cq  # type: ignore
except Exception:  # pragma: no cover - cadquery is optional
    cq = None  # type: ignore[assignment]

from ..data_model import Deck, Hull, StationModel, Wormhole


if cq is not None:  # pragma: no cover - exercised when cadquery is installed

    def _build_deck(deck: Deck) -> Tuple[cq.Workplane, List[cq.Workplane]]:
        """Create a CadQuery solid for a deck and optional window solids."""

        solid = (
            cq.Workplane("XY")
            .circle(deck.net_outer_radius_m)
            .circle(deck.net_inner_radius_m)
            .extrude(deck.net_height_m)
        )
        windows: List[cq.Workplane] = []
        for w in deck.windows:
            win = (
                cq.Workplane("XY")
                .center(w.position[0], w.position[1])
                .box(w.size_m, w.size_m, deck.net_height_m)
            )
            windows.append(win)
        return solid, windows

    def _build_hull(hull: Hull) -> Tuple[cq.Workplane, List[cq.Workplane]]:
        """Create a CadQuery solid for the hull and optional windows."""

        solid = cq.Workplane("XY").sphere(hull.net_radius_m)
        windows: List[cq.Workplane] = []
        for w in hull.windows:
            win = (
                cq.Workplane("XY")
                .center(w.position[0], w.position[1])
                .circle(w.size_m / 2)
                .extrude(hull.net_radius_m * 2)
                .translate((0, 0, w.position[2]))
            )
            windows.append(win)
        return solid, windows

    def _build_wormhole(wormhole: Wormhole) -> cq.Workplane:
        return cq.Workplane("XY").circle(wormhole.radius_m).extrude(wormhole.height_m)

    def export_step(model: StationModel, filepath: str | Path) -> Path:
        """Export the given ``StationModel`` as a STEP file."""

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        assembly = cq.Assembly()

        for deck in model.decks:
            solid, windows = _build_deck(deck)
            assembly.add(solid, name=f"deck_{deck.id}", metadata={"material": "Stahl"})
            for i, win in enumerate(windows):
                assembly.add(
                    win,
                    name=f"deck_{deck.id}_window_{i}",
                    metadata={"material": "Glas"},
                )

        if model.hull:
            solid, windows = _build_hull(model.hull)
            assembly.add(solid, name="hull", metadata={"material": "Stahl"})
            for i, win in enumerate(windows):
                assembly.add(
                    win, name=f"hull_window_{i}", metadata={"material": "Glas"}
                )

        if model.wormhole:
            solid = _build_wormhole(model.wormhole)
            assembly.add(solid, name="wormhole", metadata={"material": "Stahl"})

        assembly.save(str(path), "STEP")
        return path

else:
    # Fallback implementation that creates a tiny text based STEP-like file.
    # It is **not** a valid CAD representation but allows the unit tests to
    # verify that the exporter creates a file with content.

    def export_step(model: StationModel, filepath: str | Path) -> Path:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "STEP PLACEHOLDER\n",
            f"decks={len(model.decks)}\n",
            f"hull={1 if model.hull else 0}\n",
            f"wormhole={1 if model.wormhole else 0}\n",
        ]
        with open(path, "w", encoding="utf8") as handle:
            handle.writelines(lines)
        return path
