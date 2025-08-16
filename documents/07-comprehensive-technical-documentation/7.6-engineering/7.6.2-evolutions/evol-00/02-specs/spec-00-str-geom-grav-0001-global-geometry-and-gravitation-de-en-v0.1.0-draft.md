# SPEC-00-STR-GEOM-GRAV-0001 – Global Geometry & Gravitation *(EVOL-00, 127 m)*

**Status:** DRAFT **Version:** v0.1.0 **Datum:** 2025-08-16
**Scope:** Geometrie der Sphere Space Station **Earth ONE** (Außendurchmesser **127,00 m**), Hüllenaufbau (**0,50 m**), Deck-Bänder, künstliche Gravitation $a(r)=\omega^2 r$, Komfort-/Wohlfühlmodelle (grav-basiert + umweltbasiert), Tabellen mit aktuellen Werten je Deck inkl. Verweilzeit-Kategorien.
**Spin-Kalibrierung (EVOL-00):** **1 g** $(g_0=9{,}80665\,\mathrm{m/s^2})$ bei **r = 38{,}00 m** ⇒ $\omega=\sqrt{g_0/38{,}00}=0{,}50801\,\mathrm{s^{-1}}$ ⇒ **4,852 rpm**.

---

## 1. Station & Hülle (Geometrie, Materialien)

* **Stationsform:** Kugel, **Außendurchmesser 127{,}00 m** → **Außenradius 63{,}50 m**.
* **Druckhülle („Hull“):** nominelle Dicke **0{,}50 m**; Schichten (außen→innen): **MMOD-Bumper** (Whipple/Stuffed-Whipple), Standoff/MLI, **Druckwand** (SiC-Verbund), innen Servicekanäle/Verkleidung.
* **Primärmaterialien:** Tragstruktur **SiC-Verbund** (lokal Stahl/Inconel an Lastknoten/Öffnungen); thermische Füll-/Isolationslagen **MLI/Aerogel/Polyimid**.
* **Sichtöffnungen:** optische Stacks (Fused Silica/Borosilikat; Evaluierung ALON/Spinell für Kick/Scratch-Panes), **Außenschotts/MDPS-Shutters** analog bemannter LEO-Module.
* **Polar/Axial:** **DECK 000 („Wormhole“) –** Mikro-g-Korridor über die **127,00 m** Achse (Docking/Transfer).

> **Normative Hinweise:** MMOD-Auslegung per Stuffed-Whipple-Gleichungen; Umwelt-/Habitability-Leitwerte gem. **NASA-STD-3001 Vol. 2** (akt. Revision). Siehe Referenzen \[1–3].

---

## 2. Künstliche Gravitation – Formeln (SI)

* **Zentrifugalbeschleunigung:** $\,a(r)=\omega^2 r\,$ mit $r$ in m, $\omega$ in s⁻¹.
* **Coriolisbeschleunigung:** $\,|a_\mathrm{cor}|=2\,\omega\,v\,$ für Bewegung mit Geschwindigkeit $v$ relativ zur Struktur.
* **Vertikal-Gradient (Kopf↔Fuß, stehende Person $h$):** $\Delta a/a \approx h/r$ (aus $a=\omega^2 r$, $a_\text{head}=\omega^2(r-h)$).
* **rpm-Bezug:** $\mathrm{rpm}=\omega\cdot 60/(2\pi)$.

---

## 3. EVOL-00 „Spin-Law“

**Sollwert:** $a=9{,}80665\,\mathrm{m/s^2}$ bei $r=38{,}00\,\mathrm{m}$.
**Ergebnis:** $\omega=0{,}50801\,\mathrm{s^{-1}}$ ⇒ **4,852 rpm**.
**Human Factors (Kurzlage):** \~**4 rpm** gelten als robust für breite Populationen; höhere Raten sind mit **Adaption/Training** möglich (Kurz-/Langzeitstudien). Siehe \[7], \[8].

---

## 4. Deck-Geometrien (EVOL-00)

* **Deck-Band-Raster:** konzentrische Bänder **à 3{,}50 m**, beginnend bei **10{,}50 m** bis zur Innenhülle **63{,}00 m**.
* **Decks:**
  **001** 10,50–14,00 m · **002** 14,00–17,50 m · **003** 17,50–21,00 m · **004** 21,00–24,50 m · **005** 24,50–28,00 m · **006** 28,00–31,50 m · **007** 31,50–35,00 m · **008** 35,00–38,50 m · **009** 38,50–42,00 m · **010** 42,00–45,50 m · **011** 45,50–49,00 m · **012** 49,00–52,50 m · **013** 52,50–56,00 m · **014** 56,00–59,50 m · **015** 59,50–63,00 m.

### 4.1 g-Tabelle (Boden/Mitte/Decke pro Deck, EVOL-00, $\omega=0{,}508\,\mathrm{s^{-1}}$ ≈ 4,852 rpm)

> **Konvention:** „Boden“ = äußere Deckgrenze (max. r); „Decke“ = innere Deckgrenze (min. r).
> **Einheiten:** m/s² und in **g₀** (Erde = 1,000).
> **Berechnung:** $a(r)=\omega^2 r = g_0 \cdot r/38{,}00$. **Δg** (Kopf–Fuß) am Boden mit $h=2{,}0\,\mathrm{m}$: $100\cdot h/r_\text{floor}$.

| Deck | r\_in → r\_mid → r\_out (m) | g\_floor (m/s² / g₀) | g\_mid (m/s² / g₀) | g\_ceiling (m/s² / g₀) | Δg\_Kopf-Fuß am Boden |
| ---: | --------------------------: | -------------------: | -----------------: | ---------------------: | --------------------: |
|  001 |       10.50 → 12.25 → 14.00 |        3.613 / 0.368 |      3.161 / 0.322 |          2.710 / 0.276 |               14.29 % |
|  002 |       14.00 → 15.75 → 17.50 |        4.516 / 0.461 |      4.065 / 0.414 |          3.613 / 0.368 |               11.43 % |
|  003 |       17.50 → 19.25 → 21.00 |        5.419 / 0.553 |      4.968 / 0.507 |          4.516 / 0.461 |                9.52 % |
|  004 |       21.00 → 22.75 → 24.50 |        6.323 / 0.645 |      5.871 / 0.599 |          5.419 / 0.553 |                8.16 % |
|  005 |       24.50 → 26.25 → 28.00 |        7.226 / 0.737 |      6.774 / 0.691 |          6.323 / 0.645 |                7.14 % |
|  006 |       28.00 → 29.75 → 31.50 |        8.129 / 0.829 |      7.678 / 0.783 |          7.226 / 0.737 |                6.35 % |
|  007 |       31.50 → 33.25 → 35.00 |        9.032 / 0.921 |      8.581 / 0.875 |          8.129 / 0.829 |                5.71 % |
|  008 |       35.00 → 36.75 → 38.50 |        9.936 / 1.013 |      9.484 / 0.967 |          9.032 / 0.921 |                5.19 % |
|  009 |       38.50 → 40.25 → 42.00 |       10.839 / 1.105 |     10.387 / 1.059 |          9.936 / 1.013 |                4.76 % |
|  010 |       42.00 → 43.75 → 45.50 |       11.742 / 1.197 |     11.291 / 1.151 |         10.839 / 1.105 |                4.40 % |
|  011 |       45.50 → 47.25 → 49.00 |       12.645 / 1.289 |     12.194 / 1.243 |         11.742 / 1.197 |                4.08 % |
|  012 |       49.00 → 50.75 → 52.50 |       13.549 / 1.382 |     13.097 / 1.336 |         12.645 / 1.289 |                3.81 % |
|  013 |       52.50 → 54.25 → 56.00 |       14.452 / 1.474 |     14.000 / 1.428 |         13.549 / 1.382 |                3.57 % |
|  014 |       56.00 → 57.75 → 59.50 |       15.355 / 1.566 |     14.904 / 1.520 |         14.452 / 1.474 |                3.36 % |
|  015 |       59.50 → 61.25 → 63.00 |       16.258 / 1.658 |     15.807 / 1.612 |         15.355 / 1.566 |                3.17 % |

> **Hinweise:**
> • **1 g** liegt exakt bei **r = 38{,}00 m** (innerhalb **Deck 008** zwischen Mitte und Boden).
> • Werte linear in $r$; Rundung auf 3 Dezimalstellen (intern ≥ 1e-6).

---

## 5. Rechen- & Rundungsregeln

* **Primärgleichung:** $a(r)=g_0\cdot r/38{,}00$.
* **Rundung:** Anzeige auf **3 Nachkommastellen** (m/s²) bzw. **3 Dezimal** in g₀; interne Pipeline **double-precision**.
* **Personenhöhe für Δg:** $h=2{,}0\,\mathrm{m}$ (stehend).

---

## 6. „Gravitations-Wohlfühlformel“ $C_g$

$$
C_g = 0{,}50\,C_g^{(a)} + 0{,}25\,C_g^{(\nabla)} + 0{,}15\,C_g^{(\mathrm{cor})} + 0{,}10\,C_g^{(\omega)}.
$$

* **Ziel-g-Abweichung:** $C_g^{(a)}=1-|g-g_\mathrm{pref}|/g_\mathrm{pref}$, mit $g_\mathrm{pref}\approx 0{,}9\,g_0$.
* **Vertikal-Gradient:** $C_g^{(\nabla)}=1-(\Delta g/g)/0{,}20$ (linear bis 20 % toleriert).
* **Coriolis (typ. v=1 m/s):** $C_g^{(\mathrm{cor})}=1-\frac{2\omega v}{0{,}2\,g_0}$.
* **Spin-Term:** $C_g^{(\omega)}=1-\max(0,(\mathrm{rpm}-4)/2)$.

---

## 7. „Umwelt-Wohlfühlformel“ $C_\mathrm{env}$ & Gesamtwert

* **Umwelt-Güte:** $C_\mathrm{env}=\prod_i f_i(x_i)$, $i\in\{$Noise, CO₂, T/RH, Lux, Crowd, Light-Cycle$\}$; $x_i$ in **SI**.
* **Gesamt:** $C=0{,}7\,C_g+0{,}3\,C_\mathrm{env}$.
* **Leitnormen:** **NASA-STD-3001 Vol. 2** (Habitability, Health & Performance) – aktuellste Revision.

---

## 8. Wohlfühlen (Grav + Umwelt)

### 8.1 Gravitative Wohlfühlmatrix (EVOL-00)

**Kategoriegrenzen:** **A** ≥ 0,85 · **B** 0,70–0,85 · **C** 0,55–0,70 · **D** 0,40–0,55 · **E** 0,25–0,40.
**Hinweis:** Bei **4,852 rpm** wirken **Coriolis** und **Spin-Term** stärker als bei ≤ 4 rpm; Komfort-Peak liegt **nahe 0,9 g** (Decks 006–009).

|    Deck |     $C_g$ | Kat. | Empfohlene Nutzung / Verweilzeit (Richtwert)                           |
| ------: | --------: | :--: | ---------------------------------------------------------------------- |
|     001 |      0.36 |   E  | Transit, Technik-Gänge, ≤ 2 h; Kopfbewegungen langsam.                 |
| 002–005 | 0.45–0.67 |  D–C | Werkstätten/Logistik, 4–8 h (innen höherer $C_g$); Training empfohlen. |
| 006–009 | 0.73–0.79 |   B  | Wohnen/Arbeit gemischt, bis 16 h; sehr gute Alltagstauglichkeit.       |
| 010–014 | 0.49–0.68 |  C–D | Lab/Office/Produktion, 4–8 h; Pausen alle 2 h.                         |
|     015 |      0.44 |   D  | Schwerlast/kurze Einsätze, ≤ 4 h; Konditionierung sinnvoll.            |

*Numerik nach Kap. 6 (Formel & Gewichte) und Kap. 4/5 (g-Profile). Forschungslage: **\~4 rpm** robust, höhere Raten mit **Adaption/Training** möglich.* **(\[NSS]\[7], \[PMC]\[8])**

### 8.2 Umwelt-Wohlfühlen (Leitplanken)

* **Noise:** ≤ NC-50 in Arbeitsbereichen, Schlaf ≤ Hintergrund+10 dB.
* **CO₂:** Leitwerte gem. NASA-STD-3001; alarmgestützte Lüftungs-/Absorptionspfade.
* **Licht:** zirkadiane Profile, Lux-Zonen nach Tätigkeit.
* **Dichte/Privatsphäre:** Zielwerte nach Funktionsbereich (Crew/Visitor/OPS).

---

## 9. Sektoren-Layout & Systemintegration (DECK 013–015)

**Sektorierung:** 12 × 30° (A…L). **Radiale Druck/Brand-Schotts** entlang Sektorgrenzen; **HL-Schächte** @ 0°/90°/180°/270°, **PAX-Schächte** @ ±22.5° etc.; **Servicetunnel** doppelt (inner/outer ring). **VENT/BOP** radial (keine tangentiale Druckentlastung). **HZ-Zonen:** HZ-1 normal, HZ-2 erhöht (Energie/Heiß), HZ-3 kritisch (Nuklear/Kryo/Explosion).

### 9.1 Deck-Rollen (Kurz)

* **DECK 013 –** Puffer/Service (Schild-Wasser, HX-Galerien, Dekon).
* **DECK 014 –** Nuklear-Primär (SMR-Containments, Primärkreise) + Power-Conversion/Verteilung.
* **DECK 015 –** Tankfarm & Thermik (Wasser-Großspeicher, Sekundär/Tertiär-Loops, Gase; Kryo bevorzugt hull-mounted).

### 9.2 Tabellen (Auszug)

**DECK 015 – Tankfarm & Thermik (HZ-Schwerpunkte, D/E-Verweilzeit)**

| Sektor |  HZ | Primärfunktion            | Kern-Equip               | Schächte | Vent/Relief        | Kernauszüge Interfaces    |
| :----: | :-: | ------------------------- | ------------------------ | -------- | ------------------ | ------------------------- |
|    A   |  2  | Wasser-Puffer / Heat-Sink | 2× WTR 150 m³, HX-Module | HL-0     | BOP-015-A          | THM SecLoop-N; PWR DC-B1  |
|    E   |  3  | **Gase (O₂/N₂)** getrennt | Verbund-Flaschenbänke    | –        | **VENT-015-E→All** | GAS O₂/N₂-Header; SAFE EX |
|    F   |  3  | **Kryo-Interface**        | Manifolds → Hull-Pods    | –        | VENT-015-F         | THM Cryo-Manifold         |
|    K   |  2  | Wasser-Schildring         | Ringtank 250 m³          | –        | BOP-015-K          | THM Tie-in 014            |

**DECK 014 – SMR & Conversion (kritisch, D/E-Verweilzeit)**

| Sektor |   HZ  | Primärfunktion                | Kern-Equip            | Schächte | Vent/Relief                 | Kernauszüge Interfaces        |
| :----: | :---: | ----------------------------- | --------------------- | -------- | --------------------------- | ----------------------------- |
|    A   | **3** | **SMR-Zelle-1 (Containment)** | RPV-1, Primär-Loop-N  | HL-0     | **VENT-014-A→All** + Filter | THM Pri→Hull-HX-N; SAFE ESFAS |
|    G   | **3** | **SMR-Zelle-2 (Containment)** | RPV-2, Primär-Loop-S  | HL-180   | **VENT-014-G→All** + Filter | THM Pri→Hull-HX-S             |
|   C/I  |   2   | Power-Conversion N/S          | Brayton/Rankine-Skids | –        | VENT-014-C/I                | PWR DC-Main N/S               |

*(Vollständige Sektor-Tabellen: interne SSOT-Anlage `…/02-specs/DECK014-015-sector-layout.md`.)*

---

## 10. Rationale (nicht-normativ)

* **Warum 014 für SMR, 015 für Tanks?** 014 (\~1,52 g mid) reduziert mechanische Lasten ggü. 015 (\~1,61 g mid) bei gleicher Nähe zur Hülle/Radiatoren. 015 bietet dafür exzellentes **Phasen-Settling** und **thermische Puffer** für Loops.
* **Sicherheitsprinzip:** keine gemeinsame Ursache – **SMR** und **H₂/CH₄** strikt getrennt (Deck/Sektor/VENT-Trennung), radiale Entlastung **direkt ins All**.

---

## 11. Offene Punkte (TBD/TBC)

* **MMOD-BLE-Feinauslegung** (Partikel-Spektrum, Winkel, Dichte) je Hull-Zone.
* **Gewichte $C_g, C_\mathrm{env}$** nach Crew-Trials feinjustieren (inkl. v-Abhängigkeit Coriolis).
* **Detail-ICDs**: VENT/BOP/PT/AL-C/HL/PAX-IDs mit Koordinaten & Prüfstatus.

---

## 12. Referenzen (Auswahl)

\[1] **NASA-STD-3001 Vol. 2** – Human Systems Integration Requirements (aktuelle Revision).
\[2] **Christiansen, E.** Meteoroid/Debris Shielding – Whipple & Stuffed-Whipple Basics (NASA/JSC).
\[3] **NASA Materials/MDPS** – Windows/Optics (Fused Silica, Borosilicate, ALON/Spinel), Cupola Shutters.
\[4] **Classical AG Physics** – Rotating frames, centrifugal/coriolis (Monograph/NTRS).
\[5] **Engineering Math** – a(r)=ω²r, rpm-Umrechnung, Gradient h/r (Lehrwerke/Notes).
\[6] **Design Ops** – Safety zoning (HZ-1/2/3), pressure-tight doors PT-A/-B, airlocks AL-C (Projektstandard).
\[7] **Globus, A.; Hall, T.** *Space Settlement Population Rotation Tolerance* (NSS – Review/Position).
\[8] **Clément, G.** *Artificial gravity as a countermeasure…* (Review, peer-reviewed; z. B. npj Microgravity).

