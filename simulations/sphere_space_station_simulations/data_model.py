"""Data transfer objects for geometry exchange."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Deck:
    """Cylinder-shaped deck of the station."""

    id: int
    inner_radius_m: float
    outer_radius_m: float
    height_m: float


@dataclass
class Hull:
    """Simple spherical hull description."""

    radius_m: float


@dataclass
class StationModel:
    """Container aggregating all geometry elements."""

    decks: List[Deck] = field(default_factory=list)
    hull: Optional[Hull] = None
