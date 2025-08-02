# Schichtmodell

```
KERNEL  -> berechnet Geometrie und Simulationen
  |
  v
ADAPTER -> exportiert Datenformate (STEP, glTF, JSON)
  |
  v
GUI     -> Anwendungen wie Blender oder Web-Viewer
```

Der KERNEL enthält die Berechnungslogik. ADAPTER wandeln interne Datenmodelle in Austauschformate. GUI-Schichten konsumieren nur diese Formate und halten keine eigene Logik vor.
