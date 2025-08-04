"""Data transfer objects for geometry exchange.

The models capture derived geometric metrics such as net radii, cylinder
lengths, base areas and volumes.  Window specifications with position,
size and count can be attached to decks or the hull.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import math


@dataclass
class Window:
    """Description of a window group."""

    position: Tuple[float, float, float]
    size_m: float
    count: int = 1


@dataclass
class Deck:
    """Cylinder-shaped deck of the station."""

    id: int
    inner_radius_m: float
    outer_radius_m: float
    height_m: float
    windows: List[Window] = field(default_factory=list)
    net_inner_radius_m: Optional[float] = None
    net_outer_radius_m: Optional[float] = None
    net_height_m: Optional[float] = None
    base_area_m2: Optional[float] = None
    volume_m3: Optional[float] = None

    def __post_init__(self) -> None:
        self.net_inner_radius_m = (
            self.inner_radius_m
            if self.net_inner_radius_m is None
            else self.net_inner_radius_m
        )
        self.net_outer_radius_m = (
            self.outer_radius_m
            if self.net_outer_radius_m is None
            else self.net_outer_radius_m
        )
        self.net_height_m = (
            self.height_m if self.net_height_m is None else self.net_height_m
        )
        if self.base_area_m2 is None:
            self.base_area_m2 = math.pi * (
                self.net_outer_radius_m**2 - self.net_inner_radius_m**2
            )
        if self.volume_m3 is None:
            self.volume_m3 = self.base_area_m2 * self.net_height_m


@dataclass
class Hull:
    """Simple spherical hull description."""

    radius_m: float
    windows: List[Window] = field(default_factory=list)
    net_radius_m: Optional[float] = None
    surface_area_m2: Optional[float] = None
    volume_m3: Optional[float] = None

    def __post_init__(self) -> None:
        self.net_radius_m = (
            self.radius_m if self.net_radius_m is None else self.net_radius_m
        )
        if self.surface_area_m2 is None:
            self.surface_area_m2 = 4 * math.pi * self.net_radius_m**2
        if self.volume_m3 is None:
            self.volume_m3 = (4 / 3) * math.pi * self.net_radius_m**3


@dataclass
class Wormhole:
    """Central cylindrical passage running through the station."""

    radius_m: float
    height_m: float
    base_thickness_m: float = 0.0


@dataclass
class StationModel:
    """Container aggregating all geometry elements."""

    decks: List[Deck] = field(default_factory=list)
    hull: Optional[Hull] = None
    wormhole: Optional[Wormhole] = None
