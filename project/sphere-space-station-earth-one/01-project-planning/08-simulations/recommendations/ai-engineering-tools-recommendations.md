---
id: ""
title: ""
version: v0.0.0
state: DRAFT
evolution: ""
discipline: ""
system: []
system_id: []
seq: []
owner: ""
reviewers: []
source_of_truth: true
supersedes: null
superseded_by: null
rfc_links: []
adr_links: []
cr_links: []
date: 1970-01-01
lang: EN
---

# 1. AI-gestützte Engineering-Tools

Diese Ausarbeitung beantwortet die Frage, welche KI-unterstützten Engineering-Tools in einer ersten Anlaufphase für das Projekt geeignet sein könnten. Sie berücksichtigt die bereits vorhandenen Python-Skripte und die Hinweise aus dem Geschäftsplan.

## 1.1 Open-Source-Werkzeuge für Simulation und Optimierung

- **poliastro** oder **GMAT** für Bahnmechanik und Missionsplanung. Beide bieten Python-Schnittstellen, sodass sie mit Optimierungsbibliotheken oder KI-Frameworks kombiniert werden können.
- **OpenMDAO** für multidisziplinäre Designoptimierung. Dieses Framework lässt sich mit maschinellen Lernverfahren koppeln, um Entwurfsparameter effizient zu erforschen.
- **FreeCAD** oder **Onshape** als kostengünstige CAD-Lösung mit Python-Scripting. Später könnten Generative-Design-Methoden ergänzt werden.

## 1.2 Visualisierung und Datenanalyse

- **Blender** wird bereits in den Empfehlungen genannt und eignet sich dank der Python-API für prozedurale Modellierung und KI-gestützte Animationspipelines.
- **TensorFlow** oder **PyTorch** können genutzt werden, um aus Simulationsdaten Vorhersagemodelle abzuleiten, zum Beispiel für Lebensunterstützungssysteme.

Diese Werkzeuge sind quelloffen oder günstig erhältlich und passen somit zum Ansatz, die frühen Projektphasen mit begrenzten Mitteln zu unterstützen. Sie helfen bei der Erstellung von "Business-Plan, Pitch-Deck und Simulationsmodelle", wie im Geschäftsplan skizziert.
