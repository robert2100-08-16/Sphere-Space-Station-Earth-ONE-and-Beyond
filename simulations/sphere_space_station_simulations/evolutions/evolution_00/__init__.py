from importlib import import_module
from types import ModuleType
import sys

# Expose modules as direct submodules to allow
# ``simulations.sphere_space_station_simulations.evolutions.evolution_00.deck000``
# style imports despite the package residing in ``modules``.
deck000: ModuleType = import_module('.modules.deck000', package=__name__)
sys.modules[__name__ + '.deck000'] = deck000

__all__ = ['deck000']
