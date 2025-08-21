# SPEC-00-STR-SYS-WORMHOLE-SAFETY-0002 — Polar Approach & Full Hazard Hardening *(EVOL-00/01)* — v0.1.0 DRAFT

**Scope:** Konstruktive „Safety-by-Design“-Maßnahmen für **DECK 000 / Wormhole** inkl. **Polar-Einflug (Nord/Süd)** sowie ein **vollständiger Hazard-Katalog** für die axialen Systeme (Explosion, Brand, Kollision, Strahlung, MMOD quer/längs, **unkontrollierter Anflug/Impact** u. v. m.).
**Bezug:** Stationen **Earth ONE** (Ø 127 m) und **Earth TWO** (Ø 254 m, inkl. Long-Capsule-Varianten).

---

## 0) Executive Summary

* **Neuer Top-Hazard:** *Unkontrollierter Anflug/Impact auf die Polar-Einflugborde.*
  → Gegenmaßnahmen: **POL-GUARD** (mehrlagiger Polar-Prallschutz), **POL-KOS/Kep-Out-Volumes** mit Autopilot-Geofencing, **Polar-Shutter (≤0,5 s)**, **Deflektions-Jets**, **Jettison/Abort-Prozeduren**, konsequent **radiale Entlastung**.
* **Safety-Architektur insgesamt:** **Mehrfach-Kompartimentierung in 2D (radial + axial/LAT)**, **inertisierte Technikzonen**, **nicht-brennbare Materialien**, **VENT/BOP nur radial**, **fail-safe geschlossene** Schotts/Türen, **kein Single Point of Failure**.
* **Härtung gegen Kaskaden:** Explosions-/Brand-Energie **lokal binden**, **Impuls aufnehmen/ableiten**, **Druck & Rauch** in Sekunden **ins All** abführen, **Scheiben/Ringe** schließen – *bevor* das Nächste kippt.

---

## 1) Designziele (Safety Envelope)

1. **Containment:** Jedes Ereignis bleibt bauabschnittsweise beherrscht (Ring-zu-Ring, Sektor-zu-Sektor).
2. **Energy-&-Mass-Management:** Druck, Rauch, Partikel **radial zur Hülle**; **keine tangentiale** Relief-Führung.
3. **Fail-Safe:** Türen/Schotts **schließen stromlos**; Aktor-USV ≥ 30 min; Doppelte Sensorik.
4. **Human Factors:** klare Flucht-/Sammelzonen (Safe-Hold-Nodes), Gegenstrom-Trennung, visuelle/akustische Guidance.
5. **Testbarkeit:** Alle Schutzfunktionen mit **Zeit- und Kapazitäts-Targets** (Schließzeiten, Vent-A, Inert-Setpoint) verifizierbar.

---

## 2) Neuer Unfalltyp: **Polar-Impact** (unkontrollierter Anflug/Einschlag)

### 2.1 Szenario & Klassen

* **PI-Light:** ≤ 10 t @ ≤ 2 m/s (Klein-Tender/Roboter)
* **PI-Medium:** 10–40 t @ 2–10 m/s (Crew/Cargo-Module)
* **PI-Heavy:** 40–120 t @ 5–20 m/s (Großschiff-Anflugfehler)
* **PI-Extreme:** > 120 t oder > 20 m/s (hoffentlich nur „design to survive, not to save vehicle“)

**Parameter:** Impuls $J=m\Delta v$, Energie $E=\tfrac12 m v^2$. *Auslegung erfolgt parametriert, nicht fahrzeugspezifisch.*

### 2.2 **POL-GUARD** – Mehrlagiger Polar-Prallschutz (konstruktiv)

1. **Sensor-Vorhang (Lidar/Radar/Optik):** 3D-Track, Health-Monitoring, Autopilot-Geofencing.
2. **Deploy-Net & Tether-Dämpfer:** ausfahrbares Fangnetz mit vielen **Shock-Absorber-Tethers** (Reißnadeln + viskoelastische Dämpfer).
   – *Energieaufnahme \~ $\sum \tfrac12 k_i x_i^2$; Tether-Hub begrenzt Relativ-Δv.*
3. **Crush-Bumper-Kragen:** Ringsegmente aus **Al-Honeycomb/Metal-Foam**; spezifische Energieaufnahme (SEA) **20–60 kJ/kg**.
   – *Erforderliche Masse $m_\text{bumper}\approx E/\text{SEA}$.*
4. **Deflection-Cone:** harte, geneigte Prallfläche → **Ablenkung out-of-axis**, Fragmente werden **aus dem Wormhole heraus** gelenkt.
5. **Polar-Shutter (0,5 s):** gepanzerte, **guillotine-artige** Innenschotten (Mehrsektor-Lamellen) – schließt die Achse.
6. **VENT/BOP-Kranz:** Sollbruch/Blow-Out-Paneele **hull-nah**; Druck/Partikel **direkt ins All**.

> **Dimensionierungshilfe (Honeycomb-Bumper):**
> Volumspezifische Absorption $W=\sigma_\text{crush}\cdot \varepsilon$. Bei $\sigma\approx2\,\text{MPa}$, $\varepsilon=0{,}5$ → $W\approx1\,\text{MJ/m}^3$.
> *Beispiel:* $E=50\,\text{MJ}$ (z. B. 50 t @ 14 m/s) ⇒ **\~50 m³** Crush-Material (auf Sektoren verteilbar).

### 2.3 **POL-KOS/Kep-Out-Volumes & Autopilot-Logik**

* **Approach Ellipsoid** + **Keep-Out Sphere** polar; **Single-Vehicle-Between-Rings** (keine Doppelbelegung).
* **Hard Interlocks:** Bei **KOS-Verletzung** → *Station* schließt **Polar-Shutter**, zündet **Deflection-Jets**, aktiviert **Deploy-Net**.

---

## 3) Komplett-Hazard-Katalog (DECK 000 / axial)

**Mechanisch/Kinetisch**

* H-E1: Explosion am Docking-Ring (anliegendes Schiff)
* H-E2: Brand/Flashover an angedocktem Schiff
* H-E3: Fahrzeug-Kollision im Wormhole (axial)
* **H-E4: Polar-Impact (unkontrollierter Anflug/Einschlag)**
* H-E5: Strukturelles Versagen eines Ring-Adapters / Quick-Release
* H-E6: Trümmer/„Runaway“ nach Jettison im Näherungsbereich

**Umwelt/Exogen**

* H-U1: **Sonnenwind/SPE/CME** (Strahlungs-Spike)
* H-U2: **MMOD quer** (seitlicher Durchschlag Tubus/Ring)
* H-U3: **MMOD längs** (axial entlang der Achse)
* H-U4: Weltraumschrott-Schwarm (Kollisionskaskaden-Risiko)

**Prozess/Medien**

* H-P1: O₂-Anreicherung / Inertgas-Fehlfunktion
* H-P2: Kryo-Leck (H₂/O₂/N₂/Ar) → Kälte/EX-Risiken
* H-P3: Batterie-Thermal-Runaway (Carrier/Andock-Vehikel)
* H-P4: Giftige Medien (NH₃/Monosilan etc.) aus Nutzlast

**Systemisch/OPS/IT**

* H-S1: Stromausfall/USV-Versagen der Aktoren
* H-S2: Sensorik-Blindheit (Radar/Lidar/Optik)
* H-S3: **Cyber/Spoofing** (GN\&C/Transponder/Beacons)
* H-S4: Human-Factor (Fehlerhafte Freigabe/Prozedur)
* H-S5: Software-Regression (Update bricht Interlocks)

> **Für jeden Hazard** führen wir **S (Severity 1–5)**, **L (Likelihood A–E)**, **R = S×L**, **Mitigation (Design/OPS)**, **V\&V** in einer Tabellen-SSOT (CSV) – bereit zum Risikoreview.

---

## 4) Design-Maßnahmen (Layered Hardening)

### 4.1 Kompartimentierung & Schotts

* **Ring-zu-Ring**: PT-A (Haupt), PT-B (Service), AL-C (Airlock) – *fail-safe zu*, kaskadierbar; Δp-Rating ≥ 1 atm sektorweise.
* **LAT-Scheiben (axial):** schließen **S40/EQ/N40** (EVOL-01) → **Rauch/Heißgas-Kappen**, *kein Voll-Δp* (Equalizer).

### 4.2 VENT/BOP

* **Nur radial** zur Hülle; dimensioniert auf **choked flow**.
  $\dot m = C_d A P_0 \sqrt{\tfrac{\gamma}{RT}}\big(\tfrac{2}{\gamma+1}\big)^{\!\frac{\gamma+1}{2(\gamma-1)}}$
  → **A\_VENT** je Ring so, dass $p \rightarrow p_\text{safe}$ in **Δt\_max** (Stationsziel, z. B. ≤ 3–5 s).

### 4.3 Feuer & Inertisierung

* **Ar/N₂-Flutung** ringweise; O₂-Setpoint **≤ 12–15 Vol-%** in **≤ N s**; nicht-brennbare Auskleidung, EX-Zonierung.

### 4.4 Fenster/MDPS/Shutter

* Multilayer-Stacks, **Shutter ≤ 0,5 s** für E4/E5/E6 (SPE/MMOD), außen **MDPS-Shades**.

### 4.5 Docking-Ringe (Blast/Quick-Release)

* **Opfer-Zonen** (frangible) + **Blast-Cradle** (Sandwich-Kragen), **Jettison** mit Rückzugs-Shutter; integrierte **Deflektoren**.

### 4.6 *Neu:* **POL-GUARD** am Polar-Einflug

* **Deploy-Net + Tethers**, **Crush-Bumper**, **Deflection-Cone**, **Polar-Shutter**, **VENT-Kranz** – s. 2.2.

### 4.7 Traffic-Separation & Interlocks

* **Nord = Arrivals, Süd = Departures**, **Ein-Fahrzeug-Slot zwischen zwei Ringen**, GN\&C-Beacon-Pflicht, „rogue transponder“ → sofortige **POL-Shutter**-Schließung + **Deflection-Jets**.

### 4.8 Cyber-Resilienz

* Out-of-Band-Beacons, **AuthN/AuthZ** für Freigaben, Air-Gap für Safety-PLC, „last-known good“-Rollback.

---

## 5) Parametrische Auslegung (Formeln)

### 5.1 Polar-Bumper (Crush-Energie)

* **Eingang:** $m, v$ → $E=\tfrac12 m v^2$.
* **Bumper-Bedarf:** $V_\text{crush}\approx E/W$ mit $W$ (MJ/m³) aus Materialdaten.
* **Masse-Daumen:** $m_\text{bumper}\approx E/\text{SEA}$ (SEA=20–60 kJ/kg).

### 5.2 Fangnetz + Tethers

* **Zielhub** $x$ pro Tether; **Energie** $E\approx\sum \tfrac12 k_i x_i^2$.
* **Grenzlast** → $F_\text{max}=\sum k_i x_i$ ≤ stationäre Grenzkräfte (Ankerpunkte).
* *Praktisch:* 8–16 Tethers, je **viskoelastischer Dämpfer** (Hysterese) + Reißelement („fuse“) zur Lastspitzenbegrenzung.

### 5.3 Polar-Shutter (Impuls)

* **Impulsreserve:** $J_\text{shutter}\ge m\Delta v$ der zu erwartenden Fragmentlast *auf den Schließweg*.
* **Schließzeit:** $t_\text{shut}\le 0{,}5\,\text{s}$ bei **E4/E5/E6**-Trigger; Kraft-/Leistungsbudget ergo dimensionieren.

---

## 6) Prüf- & Abnahmekriterien (V\&V)

* **PT-A/PT-B/AL-C:** Schließzeit lokal ≤ 3 s, kaskadiert ≤ 8 s; Dichtheit Δp ≥ 1 atm (Ring-Weise).
* **VENT/BOP:** Nachweis $A_\text{VENT}$ → $p \downarrow p_\text{safe}$ in Δt\_max; Funktions-Drills (kalte Gas-Runs + CFD).
* **Shutter:** 100 % End-to-End-Tests (SPE/MMOD/Polar-Alarm) mit High-Speed-Log; Ziel ≤ 0,5 s.
* **POL-GUARD:** Drop-/Schlitten-Versuche (E-Klassen), Netz-Schlusstests, Tether-Dämpfer-Charakteristik, Cone-Deflection-Mapping.
* **Cyber:** Red-Team-Tests (Spoofing/Replay), Safety-PLC-Failover.

---

## 7) Risiko-Matrix (Beispiel-Ausschnitt)

| Hazard                | S (1–5) | L (A–E) |   R   | Primär-Mitigation                         |
| --------------------- | ------: | :-----: | :---: | ----------------------------------------- |
| H-E1 Explosion Dock   |       5 |    C    | **H** | Ring-Containment, VENT/BOP, Quick-Release |
| **H-E4 Polar-Impact** |       5 |   B–C   | **H** | **POL-GUARD, Shutter, KOS, Deflection**   |
| H-U3 MMOD längs       |       4 |    C    |   H   | Shutter-Kaskade, Spall-Liner              |
| H-S3 Cyber/Spoof      |       4 |    C    |   H   | AuthN/PLC-Air-Gap, OOB-Beacons            |
| H-P2 Kryo-Leck        |       4 |    C    |   H   | EX-Zonen, Inert, VENT                     |

(*Vollständige Matrix als CSV/SSOT führen.*)

---

## 8) Umsetzung & Roadmap

* **EVOL-00 (127 m):** Polar-Shutter + KOS sofort; **POL-GUARD (light)** (Crush-Kragen + Net).
* **EVOL-01 (254 m Kugel):** **POL-GUARD (medium)** + Deflection-Cone + stärkere VENT/BOP-Kranz.
* **EVOL-01 Long Capsule:** **POL-GUARD (heavy)** + 2. Fußring im Core; Dock-Throats auf ≥ 16–20 m, wenn Innendocking.

---
