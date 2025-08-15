# Evolutions – DECK000

**EVOL-00 v0.1.1** implements the baseline axial tube geometry for **DECK000**
without window cut-outs:

- Length 127 m; barrel OD 22 m, ID 20 m
- Six docking rings (10 m each) with constricted **ID 10 m**, first ring at **3.5 m**, **pitch 20 m**
- Window-tube spans (10 m) between rings; 3.5 m service clearances at both ends
- Export: **OBJ**, **CSV** table (Table-1 equivalent) and **glTF** with basic materials

Per SSOT, EVOL‑00 includes rectangular window units between the docking rings.
These apertures will be added in **v0.1.1**.

## Usage

```bash
python -m simulations.sphere_space_station_simulations.evolutions.evo0_deck000
```

Artifacts:

- `simulations/results/deck000_ev0/deck000_ev0.obj`
- `simulations/results/deck000_ev0/deck000_ev0_segments.csv`
- `simulations/results/deck000_ev0/deck000_ev0.glb`

Import the OBJ or glTF in Blender/CAD and proceed with ring-level detailing.

## Notes

- Mesh is a double-skin tube (outer + inner surface), no end caps (for contiguous joining).
- Radial tessellation default `96` (configurable in `Deck000Params.radial_segments`).
- All distances in **meters**; z-axis points North→South (z=0 at North interior face).
