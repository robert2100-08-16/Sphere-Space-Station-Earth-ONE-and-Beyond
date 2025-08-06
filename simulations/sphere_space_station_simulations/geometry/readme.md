# 1. Geometry Package

Contains core geometry classes and calculations used by the simulation modules.

- `deck.py` implements the `SphereDeckCalculator` used to compute deck data. It
  can optionally generate support columns for each deck and equatorial docking
  port positions.
- `hull.py` provides `calculate_hull_geometry` which derives the outer hull mesh
  and `calculate_docking_port_positions` to place docking ports.
