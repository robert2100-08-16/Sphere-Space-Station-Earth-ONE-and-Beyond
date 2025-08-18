# SPEC-01-STR-GEOM-GRAV-E2-LCAP-0001-earth-two-long-capsule-D254m-L508m—v0.1.0-DRAFT
> Earth TWO “Long Capsule” *(EVOL-01, Ø 254 m × L 508 m)* Global Geometry & Gravitation

**Scope:** Zylindrisch-kapselartige Station mit Hemisphären-Endkappen, **Außendurchmesser 254,00 m** (R=127,00 m), **Gesamtlänge 508,00 m** (Zylinderlänge ≈ **254 m** + 2× Halbkugel). Hülle nominell **0,50 m**. Spin-Gesetz, 1 g-Kalibrierung („best-fit“), Habitat-Zonen, Struktur-Raster (Längs- & Breitengrade), Safety/Kompartmentierung, Transportachsen, Kapazitäts-Herleitung.

---

## 1) Geometrie & Hülle

* **Form:** Zylinder (Innenradius $R_h=126{,}50\,\mathrm{m}$) + zwei hemisphärische Endkappen.
* **Zylinder-Länge innen:** $L_c \approx 254{,}0\,\mathrm{m}$. **Gesamtlänge:** $508{,}0\,\mathrm{m}$.
* **„Wormhole“-Korridor:** axialer Mikro-g-Tunnel (ID \~**20 m**), durchgehend Süd↔Nord; Docking in beiden Endkappen.
* **Axiale Rasterung:** **16 Blöcke** à **31,75 m** (Z00…Z15) für Layout, Fertigung, Safety-Sperr-Zonen.
* **Hülle:** 0,50 m (Stuffed-Whipple-Außenlage / MLI / Druckschale SiC-Verbund); Fenster nur in ausgewählten Habitatzonen (Schotts/MDPS-Shutters).

---

## 2) Spin-Gesetz & „1 g best-fit“

Grundgleichung: $a(r)=\omega^2 r$, $\mathrm{rpm}=\omega\cdot\frac{60}{2\pi}$.

**Zwei sinnvolle Kalibrierungen (beide komfortabel):**

* **Option A – Hüllen-1 g (rpm-minimal):** **1 g bei $r=R_h=126{,}50\,\mathrm{m}$**
  $\omega=\sqrt{\tfrac{g_0}{126{,}5}} \approx 0{,}2785\,\mathrm{s^{-1}}$ → **2,66 rpm**.
  *Pro:* Minimaler Coriolis, Außenring exakt 1 g. *Kontra:* 5–10 m innen schon <1 g.

* **Option B – Wohnring-„best-fit“:** **1 g bei $r=120{,}00\,\mathrm{m}$**
  $\omega=\sqrt{\tfrac{g_0}{120{,}0}} \approx 0{,}2859\,\mathrm{s^{-1}}$ → **2,73 rpm**.
  *Pro:* 115–126,5 m liefert **0,96–1,05 g** (breiter Sweet-Spot). *Kontra:* minimal höhere rpm.

**Empfehlung EVOL-01:** **Option B (2,73 rpm)** für einen breiten, gleichmäßig „erdigen“ Wohnring; **Option A** als Alternate-Mode.

> **Kopf-Fuß-Gradient** am „Boden“ (h=2,0 m):
> bei r=126,5 m ≈ **1,58 %**, bei r=120,0 m ≈ **1,67 %** (sehr komfortabel).
> **Coriolis:** Bewegung **entlang der Achse** (parallel ω) → **≈0**; Querbewegungen moderat bei \~2,7 rpm.

---

## 3) Zonen & Nutzung

**Radial (r):**

* **Außenring (r≈115–126,5 m):** **Haupt-Habitat** (Wohnen, Schulen, Handel, Kultur, Parks) bei \~0,96–1,05 g (Option B).
* **Mittelring (r≈80–115 m):** **Arbeit/Agro/Labore**, 0,64–0,96 g; gute Ergonomie, reduzierte Lasten.
* **Innenring (r<80 m):** **Industrie/F\&E/Sport** (0–0,64 g), Bühnen, Atrien; Übergänge zur **Mikro-g-Achse**.

**Axial (Z-Blöcke Z00…Z15, je 31,75 m):**

* **Z00/Z15 (Endkappen):** Docking, Fracht, Hangars, Service.
* **Z01–Z03 & Z12–Z14:** Technik/THM/Power-Ringe, EX-Zonen separiert.
* **Z04–Z11 (Mitte):** Habitat-Distrikte (je \~32 m Länge), mit Plazas, Parks und „High-Street“ tangential.

---

## 4) Strukturkonzept (Grid C: Längs **+** Breitengrade)

* **Längsgrade:** 12 radiale **Sektorschotten** (A–L, 30°), druck-/brandfähig (Δp ≥ 1 atm sektorweise), PT-A/B-Türen, AL-C-Schleusen.
* **Breitengrade (LAT):** **Ring-Diaphragmen** in jedem Z-Block-Stoß (31,75 m); zusätzlich **Haupt-LAT** in Z04/Z08/Z12.
* **Rahmenraster:** sekundäre **Frame-Ringe** etwa alle **7,9 m** (¼-Block) für lokale Steifigkeit & Paneelgrößen.
* **Vent/Relief:** **radial** zur Hülle (VENT/BOP), keine tangentiale Entlastung.
* **Membranspannungen (Zylinder):** $\sigma_{\theta}\approx \tfrac{p\,R_h}{t}$ (Reifenspannung), $\sigma_{z}\approx \tfrac{p\,R_h}{2t}$ (Längs); mit $p≈101\,\mathrm{kPa}$, $R_h=126{,}5\,\mathrm{m}$, $t=0{,}5\,\mathrm{m}$ → $\sigma_{\theta}\approx 25{,}6\,\mathrm{MPa}$ (gut beherrschbar für Verbund/Metall-Liner mit FoS).

---

## 5) Transport & Logistik

* **Axial (µg):** Zentralkorridor (Wormhole) mit **Maglev-Spine** (Crew/Logistik), Fast-Transit Endkappe↔Endkappe.
* **Tangential (1 g-Boden):** **Ring-Tram** (2–3 Linien) pro Habitat-Gürtel; Fuß-/Radwege entlang „High-Street“.
* **Radial:** **Lift-Spokes** (PAX/HL) in jedem zweiten Sektor (6 Hauptspeichen) zwischen µg-Achse ↔ Außenring.

---

## 6) Kapazität & Flächen

* **„Erd-Boden“ am Innenhüll-Zylinder:** $A_\text{floor} ≈ 2\pi R_h \cdot L_c \approx 2\pi\cdot126{,}5\cdot508 \approx 4{,}04\times 10^5\,\mathrm{m^2}$.
  → Bei **20–40 m²/Person** ergeben sich **\~10 000–20 000 Plätze** **allein auf Bodenniveau**.
* **Terrassen (≤ 10 m radial)**: zusätzliche Ebenen bei 0,92–0,98 g (+30–60 % Fläche).
* **Fazit Kapazität:** **> 4 000** problemlos; **10 000–20 000** realistisch im EVOL-01-Ausbau (ohne Innen-„Stadtkern“ massiv zu verdichten).

---

## 7) Habitabilität (Kurzlage)

* **Komfortfenster:** 0,95–1,05 g im Außenring (Option B) → **Kat. A/B** ganztägig.
* **Coriolis:** axial quasi null; tangential moderat (≤ 2,73 rpm).
* **Akustik & Klima:** LAT-Scheiben separieren Strömungs-/Lärmzonen; Parks/Plazas als akustische „Sinks“.
* **Verweilzeiten:** Habitat unbegrenzt; Technik/EX-Zonen nach D/E-Kategorien (≤ 4 h / ≤ 2 h).

---

## 8) Beispiel-g-Profil (Option B: 1 g @ 120,0 m → 2,73 rpm)

> $g/g_0=r/120$. „Boden“ = $r=126{,}5$; „Balkon“ = $r=120$; „Galerie“ = $r=112$.

| Standort              | Radius r (m) |      g/g₀ | Hinweis                               |
| --------------------- | -----------: | --------: | ------------------------------------- |
| Boden Außenring       |        126,5 | **1,054** | kräftig „erdig“, Top für Sport/Lasten |
| Wohn-Balkon           |        120,0 | **1,000** | **best-fit**                          |
| Galerie/Park          |        115,5 |     0,962 | softer, angenehm                      |
| Agro-Ringe            |        100,0 |     0,833 | Pflanzen/leichte Arbeit               |
| Industrie/Sport innen |         80,0 |     0,667 | schwere Geräte, Labore                |
| Achse (Wormhole)      |         0–10 |       \~0 | µg-Transport/Andock                   |

**Kopf-Fuß-Δg** am Boden (2,0 m): **\~1,6 %**.

---

## 9) Safety & Kompartmentierung

* **Sektoren (A–L):** radiale Druck/Brand-Zellen (PT-A/B, AL-C); VENT/BOP **radial**.
* **LAT-Ebenen:** je Blockstoß (31,75 m) + Haupt-LAT (Z04/Z08/Z12) als **axiale Kappen** (Equalize-Philosophie, **kein Voll-Δp**).
* **EX/NUC-Zonen:** in Außen-Technikgürteln separiert; **keine** Kryo/H₂ mit Nuklear-Primär im selben Sektor/Block.

---

## 10) Nächste Schritte (konkret)

1. **Spin-Entscheidung:** Option B (2,73 rpm) als Standard, Option A (2,66 rpm) als Alternate.
2. **Z-Block-Freeze:** Funktionen Z00…Z15; Haupt-LAT in Z04/Z08/Z12.
3. **Trassenplanung:** Ring-Tram, Maglev-Spine, 6 Haupt-Liftspokes.
4. **ICD Safety:** PT-Türen/Schleusen-Katalog, Equalizer-Spezifikation, VENT/BOP-Sizing.
5. **Massen-/Struktur-Sizing:** Rahmenabstände, Paneeldicken, FoS; Fertigungs-/QC-Plan Fugen/Schraubgurte.

---