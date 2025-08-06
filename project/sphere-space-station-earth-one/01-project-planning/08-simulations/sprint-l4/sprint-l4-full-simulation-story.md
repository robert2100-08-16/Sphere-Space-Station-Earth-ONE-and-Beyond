Hier ist der überarbeitete Taskplan für die Sprintrunde L4 inklusive Abgleich mit den Dokumenten im Verzeichnis `/documents`.  Zusätzlich liste ich auf, welche Einbauten laut den technischen Dokumenten noch im geplanten Full‑Simulator fehlen.

## 🧭 Fehlende Einbauten laut Dokumentation

Die vorhandene Planung (radiale und tangentiale Aufzüge, Fahrtreppen, Brandschotts, Gyroschwungmassen, Agrikultur‑Einheiten, Wohnquartiere) deckt viele interne Transportsysteme ab, aber die Dokumente nennen weitere Systeme und Strukturen, die für ein realistisches Modell ergänzt werden sollten:

| Themenbereich                       | Einbauten aus den Dokumenten                                                                                                                                                                                                                                                                                                                           | Quelle                                                |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| **Zugang & Transport**              | – Schwerlast‑Aufzüge zusätzlich zu den Personenliften, die alle Decks verbinden. <br>– Tangentiale Förderbänder und Schienenfahrzeuge zur Materialbeförderung. <br>– Hover‑ und Kletterkanäle mit magnetischen Stiefeln und Handläufen für den Personentransport in Mikrogravität.                                                                     | Technische Spezifikation Decklayout                   |
| **Energie & Wärme**                 | – Zwei NuScale‑SMR‑Reaktoren bzw. Array von Mikroreaktoren als primäre Energiequelle; zusätzliche Reserve‑Reaktoren. <br>– Grossflächige Solarpanel‑Arrays auf den Außenhüllen. <br>– Große Flüssig‑Wärmespeicher (z. B. Salztanks) und ausfahrbare Radiatoren zur Hitzeabfuhr. <br>– Batteriebänke und Schwungmassen‑Energiespeicher für Lastspitzen. | Energie‑ und Thermalsysteme, Technische Spezifikation |
| **Sicherheit & Notfall**            | – Umfassende Feuerlöschsysteme (Inertgas, Wassernebel) und Kompartimentierung. <br>– Strahlenschutzwände und sichere Räume. <br>– Multi‑Layer‑Mikrometeoroid‑Schutzschalen. <br>– Evakuationskapseln mit autonomer Rückkehr und Sammelpunkte für Notfälle.                                                                                             | Technische Spezifikation                              |
| **Docking & Externe Logistik**      | – Zentraler Docking‑Port auf Deck 000. <br>– Fracht‑ und Abfallbays mit automatischer Verarbeitung. <br>– Shuttlesysteme für Erd‑LEO‑Transfers und Langstreckenmissionen.                                                                                                                                                                              | Technische Spezifikation                              |
| **Steuerung & Antrieb**             | – Gyroskope und Reaktionsräder zur Lagekontrolle. <br>– Elektrische Thruster für Bahnkorrekturen.                                                                                                                                                                                                                                                      | Technische Spezifikation                              |
| **Lebensunterhalt & Infrastruktur** | – Geschlossene Luft‑, Wasser‑ und Abfallrecycling‑Systeme. <br>– Hochgeschwindigkeits‑Datennetz für Kommunikation und Steuerung.                                                                                                                                                                                                                       | Technische Spezifikation                              |
| **Weitere Einrichtungen**           | – Hydroponik und Bioreaktoren als Nahrungsmittelproduktion. <br>– Medizinische Zentren, Freizeit‑ und Lernbereiche, industrielle Fertigungslabore und Recyclinganlagen.                                                                                                                                                                                | Staffing- und Facility‑Dokument                       |

Diese Punkte gehen über die bisher vorgesehene Modellierung hinaus und sollten im Full‑Simulator als optionale Module vorgesehen werden. Einige (z. B. Batterie‑ oder Datennetz) müssen nicht zwingend geometrisch detailliert sein, können aber als Platzhalter oder Funktionsobjekte integriert werden.

## 🏗️ Taskplan für Sprintrunde L4 – Full‑Simulator & Modulintegration

Nachfolgend ein Vorschlag für den Taskplan, der die oben identifizierten Zusatzsysteme einbezieht:

1. **Architekturdefinition (Story L4‑T1)**
   *Erarbeiten einer modularen `SceneModel`‑Architektur*, die alle Basiselemente (Decks, Hülle) sowie die aus den Dokumenten abgeleiteten Module abbildet. Jedes Modul soll über eine „include\_…“‑Flag per Config (TOML/JSON) ein- oder ausschaltbar sein.

2. **Modul‑Implementierung (Story L4‑T2 bis L4‑T8)**

   * **Aufzugs‑ und Transportsysteme**: Modellierung schwerer radialer Lastenaufzüge, Förderbänder/Schienensysteme und Hover‑Kletterkanäle.
   * **Energie‑Subsysteme**: Geometrische Platzhalter für SMR‑Reaktoren, Reserve‑Reaktoren, Solarpanels, Flüssig‑Wärmespeicher, Radiatorflächen und Batteriespeicher.
   * **Sicherheitsmodule**: Einbau von Brandschutzschotts, Feuerlöscheinrichtungen, Strahlenschutzblöcken, Meteoroid‑Schutzschichten und Evakuationskapseln.
   * **Docking & Fracht**: Entwicklung von Dockingports, Fracht‑ und Abfallbays sowie Shuttlesystem‑Platzhaltern.
   * **Antrieb & Stabilisierung**: Einbindung von Gyroskopen/Reaktionsrädern und Thruster‑Einheiten.
   * **Lebensunterhalt & Infrastruktur**: Hinzufügen von Air/Water/Waste‑Recycling‑Einheiten, Hydroponik‑Modulen, Bioreaktoren sowie optionalen Platzhaltern für medizinische Zentren und Industrie‑Labs.

3. **Konfigurations‑ und Steuermechanismus (Story L4‑T9)**
   Implementieren einer Konfigurationsdatei (`full_scene.toml`) und entsprechender Parser‑Logik im `prepare_full_scene.py`, die für jedes Modul ein Flag (z. B. `include_heat_storage=true`) setzt. Auf CLI‑Ebene soll `starter.py` Parameter entgegennehmen, um Komponenten einzeln zu aktivieren.

4. **Test und Validierung (Story L4‑T10)**
   Erstellen automatisierter Tests, die sicherstellen, dass beim Aktivieren/Deaktivieren einzelner Module die korrekten Objekte im glTF‑/STEP‑Export auftauchen. Dies umfasst auch den Import in Blender zur Prüfung, ob z. B. Radiatoren oder Docking‑Ports korrekt positioniert sind.

5. **Dokumentation und Guidelines (Story L4‑T11)**
   Aktualisieren des Projekt‑Readmes und einer neuen „Full‑Simulator“‑Doku, in der die verfügbaren Module, ihre Aktivierung sowie bekannte Abhängigkeiten beschrieben werden. Dazu gehören Beispiel‑Konfigs (minimal vs. komplett) und Hinweise auf die zugrunde liegenden Dokumente.

Durch diese Schritte wird gewährleistet, dass der Full‑Simulator nicht nur die Decks und Hülle abbildet, sondern auch die umfangreichen Energie‑, Sicherheits‑, Transport‑ und Lebensunterhaltssysteme, die in den technischen Dokumenten für die Sphere‑Station vorgesehen sind.
