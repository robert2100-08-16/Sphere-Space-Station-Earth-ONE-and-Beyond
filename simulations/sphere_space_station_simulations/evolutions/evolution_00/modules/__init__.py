"""
Evolutions namespace for Sphere Space Station geometry.

EVOL-00 (SemVer v0.1.0):
- Minimal, CAD-freundliche Volumendarstellung der DECK000-Röhre
- Fenster-Ausschnitte laut SSOT gehören zu EVOLUTION‑00, sind hier jedoch
  noch nicht modelliert (geplant für v0.1.1).
"""

__all__ = [
    "deck000",
]

# Import side-effect free
from . import deck000  # noqa: F401
