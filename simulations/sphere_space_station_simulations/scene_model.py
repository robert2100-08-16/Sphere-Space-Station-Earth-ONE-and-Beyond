"""Scene model linking base station geometry with optional modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .data_model import StationModel, SceneConfiguration


@dataclass
class SceneModel:
    """Complete station scene with optional modules.

    Attributes:
        station: Base geometry of the station including decks, hull, wormhole and base rings.
        config: Flags indicating which optional modules are included.

    Additional modules can be added by extending :class:`SceneConfiguration`
    with new ``include_<module>`` fields.
    """

    station: StationModel = field(default_factory=StationModel)
    config: SceneConfiguration = field(default_factory=SceneConfiguration)

    def enabled_modules(self) -> List[str]:
        """List names of modules enabled in the configuration."""
        return self.config.included_modules()
