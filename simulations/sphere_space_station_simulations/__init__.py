"""Core simulation package for the Sphere Station."""

from typing import TYPE_CHECKING

__all__ = ["SphereDeckCalculator", "StationSimulation", "calculate_hull_geometry"]

if TYPE_CHECKING:  # pragma: no cover - for type checkers only
    from .geometry.deck import SphereDeckCalculator
    from .simulation import StationSimulation
    from .geometry.hull import calculate_hull_geometry


def __getattr__(name: str):
    if name == "SphereDeckCalculator":
        from .geometry.deck import SphereDeckCalculator

        return SphereDeckCalculator
    if name == "StationSimulation":
        from .simulation import StationSimulation

        return StationSimulation
    if name == "calculate_hull_geometry":
        from .geometry.hull import calculate_hull_geometry

        return calculate_hull_geometry
    raise AttributeError(f"module {__name__!r} has no attribute {name}")
