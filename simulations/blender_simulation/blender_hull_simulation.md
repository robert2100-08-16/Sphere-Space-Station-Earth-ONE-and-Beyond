# Hull Simulation

`blender_hull_simulation.py` erzeugt eine vereinfachte Außenschale der Sphere Station. Optional lassen sich Fenster sowie die externen Aggregate Radiatoren und Solarpanels generieren.

## Verwendung

```bash
blender --python blender_hull_simulation.py -- --windows --radiators --solar-arrays
```

Ohne Optionen wird nur die Hülle erzeugt. Die Schalter `--windows`, `--radiators` und `--solar-arrays` aktivieren die jeweiligen Komponenten.

