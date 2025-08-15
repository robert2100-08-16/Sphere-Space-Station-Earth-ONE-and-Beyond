"""
Convenience runner to export all EV0 artifacts without touching package internals.

The script discovers modules in the EVOL-00 package that define a
``build_and_export_ev0`` function and runs them, writing outputs to
``simulations/results``.
"""

from __future__ import annotations

from pathlib import Path
import importlib.util
import pkgutil
import sys
from typing import Any, Callable, Dict


# Ensure repository root on sys.path for package imports
ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from typing import Iterator


def _iter_builders() -> Iterator[tuple[str, Callable[[Path], Dict[str, Any]]]]:
    """Yield ``(module_name, builder)`` pairs for EVOL-00 modules."""
    evo_dir = Path(__file__).resolve().parent.parent
    for info in pkgutil.iter_modules([str(evo_dir)]):
        if info.ispkg or info.name.startswith("_") or info.name == "scripts":
            continue
        module_path = evo_dir / f"{info.name}.py"
        module_name = (
            f"simulations.sphere_space_station_simulations.evolutions.{info.name}"
        )
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            builder = getattr(module, "build_and_export_ev0", None)
            if callable(builder):
                yield info.name, builder


def main() -> None:
    results_base = Path("simulations/results/evolutions/evolution-00")
    summaries: Dict[str, Any] = {}
    for name, builder in _iter_builders():
        if name.startswith("evo0_"):
            out_dir = results_base / f"{name.split('evo0_', 1)[1]}_ev0"
        else:
            out_dir = results_base / name
        summaries[name] = builder(out_dir)
    for mod_name, result in summaries.items():
        print(mod_name)
        for key, value in result.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
