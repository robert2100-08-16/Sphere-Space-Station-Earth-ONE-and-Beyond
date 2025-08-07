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
    material: Optional["Material"] = None


@dataclass
class Support:
    """Structural support column inside a deck."""

    deck_id: int
    position: Tuple[float, float, float]
    height_m: float
    radius_m: float
    material: Optional["Material"] = None


@dataclass
class DockingPort:
    """Docking port mounted on the hull."""

    position: Tuple[float, float, float]
    diameter_m: float
    depth_m: float
    material: Optional["Material"] = None


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
    material: Optional["Material"] = None

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
    material: Optional["Material"] = None

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
    material: Optional["Material"] = None


@dataclass
class BaseRing:
    """Structural ring attached to the hull."""

    radius_m: float
    width_m: float
    position_z_m: float
    material: Optional["Material"] = None


@dataclass
class Material:
    """Material with an optional RGBA colour."""

    name: str
    color_rgba: Tuple[float, float, float, float] | None = None


# Predefined standard materials used throughout the station model.  These
# constants provide sensible defaults and can be referenced via their German
# names in CLI options or configuration files.
STEEL = Material("Stahl", (0.8, 0.8, 0.8, 1.0))
ALUMINIUM = Material("Aluminium", (0.77, 0.77, 0.78, 1.0))
GLASS = Material("Glas", (0.5, 0.7, 1.0, 0.3))
POLYMER = Material("Polymer", (1.0, 0.2, 0.2, 1.0))

# Lookup table to resolve a material by its name.  Used by the simulation CLI to
# translate command line parameters into :class:`Material` instances.
STANDARD_MATERIALS: dict[str, Material] = {
    m.name: m for m in (STEEL, ALUMINIUM, GLASS, POLYMER)
}


@dataclass
class StationModel:
    """Container aggregating all geometry elements."""

    decks: List[Deck] = field(default_factory=list)
    base_rings: List[BaseRing] = field(default_factory=list)
    supports: List[Support] = field(default_factory=list)
    docking_ports: List[DockingPort] = field(default_factory=list)
    hull: Optional[Hull] = None
    wormhole: Optional[Wormhole] = None


@dataclass
class SceneConfiguration:
    """Flags controlling optional sub-systems in a full station scene."""

    include_transport: bool = False
    include_energy: bool = False
    include_safety: bool = False
    include_docking: bool = False
    include_propulsion: bool = False
    include_life_support: bool = False

    def included_modules(self) -> List[str]:
        """Return a list of enabled module names without the ``include_`` prefix."""
        return [
            name.removeprefix("include_")
            for name, value in vars(self).items()
            if name.startswith("include_") and value
        ]
