# Bibliotheks-Research: STEP- und glTF-Erzeugung

## STEP-Bibliotheken

### pythonocc-core
- Lizenz: LGPL/GPL
- Stärken: mächtige CAD-Kernel-Funktionen, weit verbreitet
- Schwächen: große Abhängigkeiten, steile Lernkurve

### CadQuery
- Lizenz: Apache-2.0
- Stärken: Pythonic API, integrierte Exportfunktionen (STEP, STL)
- Schwächen: weniger direkte Kontrolle über B-Rep-Details

**Entscheidung:** Für Prototypen wird `CadQuery` bevorzugt, da es eine leichtere API bietet und STEP-Export out-of-the-box unterstützt.

## glTF-Bibliotheken

### pygltflib
- Lizenz: MIT
- Stärken: schlanke Bibliothek, direkte Kontrolle über glTF-Strukturen
- Schwächen: wenig Komfortfunktionen für Mesh-Generierung

### trimesh
- Lizenz: MIT
- Stärken: hohe Abdeckung an 3D-Formaten, einfache Mesh-Erstellung
- Schwächen: größere Abhängigkeiten

**Entscheidung:** `trimesh` wird genutzt, um primitive Geometrien zu erzeugen und anschließend nach glTF zu exportieren.
