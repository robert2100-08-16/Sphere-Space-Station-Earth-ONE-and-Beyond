"""
Evolutions namespace for Sphere Space Station geometry.

EVOLUTION 0:
 - Minimal, CAD-freundliche Volumendarstellung der DECK000-Röhre
 - Ohne Boolesche Fenster-Ausschnitte (Fenster später in EV1)
"""

__all__ = [
    "evo0_deck000",
]

# Import side-effect free
from . import evo0_deck000  # noqa: F401
