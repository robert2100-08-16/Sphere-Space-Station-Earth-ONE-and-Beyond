# Software Design Decisions

Dieses Dokument fasst wichtige Architekturentscheidungen der Python-Software zusammen. Ziel ist eine langfristig wartbare Bibliothek für Berechnungen und 3D-Simulationen der Sphere Space Station.

## Abwägung der Ansätze

**Ansatz 1 – Modulare Python-Library**
- Funktionen werden in klar abgegrenzten Modulen gekapselt und können von verschiedenen Adaptern (z. B. Blender, MATLAB) genutzt werden.
- Gemeinsame Tests und eine einheitliche API erleichtern Wartung und Wiederverwendung.

**Ansatz 2 – Weiterführen des Skripts**
- Schnelle Erweiterungen sind möglich, jedoch würde das Skript mit der Zeit zu einem schwer wartbaren Monolithen anwachsen.
- Zusätzliche Adapter müssten jedes Mal individuell entwickelt werden.

## Entscheidung

Um die Simulation vielseitig nutzbar und besser testbar zu machen, wird Ansatz&nbsp;1 umgesetzt. Unter `simulations/library` entsteht eine eigenständige Python-Library. Das bestehende Skript bleibt vorerst erhalten; ein neues `deck_calculations_adapter.py` dient als Brücke zwischen Library und bisherigen Workflows.
