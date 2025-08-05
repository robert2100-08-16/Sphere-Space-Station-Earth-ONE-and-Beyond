"""Utility to ensure Blender deck scenes have required exports.

The Blender adapter expects a ``station.glb`` file in the same directory.
This helper generates the file on demand using the shared export
functions.  Optional STEP and JSON files can also be created for future
workflows.
"""

from __future__ import annotations
import logging
from pathlib import Path

from simulations.sphere_space_station_simulations import SphereDeckCalculator
from simulations.sphere_space_station_simulations.data_model import (
    StationModel,
    Deck,
    Hull,
)
from simulations.sphere_space_station_simulations.adapters import (
    export_gltf,
    export_step,
    export_json,
)


log = logging.getLogger("prep")


def _build_default_model() -> StationModel:
    """Construct a default :class:`StationModel` used for Blender previews."""

    calculator = SphereDeckCalculator(
        "Deck Dimensions of a Sphere",
        sphere_diameter=127.0,
        hull_thickness=0.5,
        windows_per_deck_ratio=0.20,
        num_decks=16,
        deck_000_outer_radius=10.5,
        deck_height_brutto=3.5,
        deck_ceiling_thickness=0.5,
    )
    calculator.calculate_dynamics_of_a_sphere(angular_velocity=0.5)

    decks = [
        Deck(
            id=int(row[SphereDeckCalculator.DECK_ID_LABEL].split("_")[1]),
            inner_radius_m=row[SphereDeckCalculator.INNER_RADIUS_LABEL],
            outer_radius_m=row[SphereDeckCalculator.OUTER_RADIUS_LABEL],
            height_m=row[SphereDeckCalculator.DECK_HEIGHT_LABEL],
        )
        for _, row in calculator.df_decks.iterrows()
    ]

    return StationModel(decks=decks, hull=Hull(radius_m=calculator.sphere_diameter / 2))


def prepare_scene(
    output_path: str | Path = "station.glb",
    *,
    create_step: bool = False,
    create_json: bool = False,
    force_new: bool = True,  # Be carefully: Whether to force creation of new files even if they exist, but if the model is different, must be set to True!
) -> Path:
    """Ensure the required glTF file exists for Blender.

    Parameters
    ----------
    output_path:
        Location of the GLB/GLTF file.  If missing, it will be generated.
    create_step, create_json:
        When set, additional STEP and JSON files are written next to the
        glTF.  Their filenames are derived from ``output_path``.
    """

    path = Path(output_path)

    if not force_new:
        # If the file already exists and we are not forcing a new one, return the existing path
        if path.exists():
            log.info("Using existing glTF file at %s", path)
            return path
    else:
        # If we are forcing a new one, delete the existing file if it exists
        if path.exists():
            path.unlink()
            log.info("Deleted existing glTF file at %s", path)

    # Ensure the parent directory exists
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        log.info("Created directory %s", path.parent)

    # If the file does not exist, we need to create it
    log.info("Preparing scene at %s", path)
    # Build the default model
    model = _build_default_model()

    path.parent.mkdir(parents=True, exist_ok=True)
    export_gltf(model, path)

    base = path.with_suffix("")
    if create_step:
        export_step(model, base.with_suffix(".step"))
    if create_json:
        export_json(model, base.with_suffix(".json"))
    return path


__all__ = ["prepare_scene"]
