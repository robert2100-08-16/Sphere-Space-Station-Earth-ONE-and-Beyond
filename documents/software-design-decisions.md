# Software Design Decisions

This document summarizes important architectural decisions of the Python software. The goal is a long-term maintainable library for calculations and 3D simulations of the Sphere Space Station.

## Evaluation of Approaches

**Approach 1 – Modular Python Library**
- Functions are encapsulated in clearly separated modules and can be used by various adapters (e.g., Blender, MATLAB).
- Shared tests and a uniform API facilitate maintenance and reuse.

**Approach 2 – Continuing the Script**
- Rapid extensions are possible, but the script would grow into a hard-to-maintain monolith over time.
- Additional adapters would have to be developed individually each time.

## Decision

To make the simulation versatile and easier to test, Approach 1 is being implemented. A standalone Python library is being created under `simulations/library`. The existing script will remain for now; a new `deck_calculations_adapter.py` serves as a bridge between the library and current workflows.

## Sources

No external sources used.
