# Sterbevergleich - Deutsche Sterbetafeln 2016-2024

Eine umfassende Analyse und Visualisierung der Sterbewahrscheinlichkeiten in Deutschland über drei Zeitperioden (2016-2018, 2020-2022, 2022-2024).

## Übersicht

Dieses Projekt analysiert die offiziellen deutschen Sterbetafeln vom Statistischen Bundesamt (Destatis) und berechnet die Sterbewahrscheinlichkeit für jedes Lebensalter-Jahrzehnt, getrennt nach Geschlecht und Zeitperioden.

**Wichtige Erkenntnisse:**
- Frauen haben durchgehend eine niedrigere Sterbewahrscheinlichkeit als Männer (außer im sehr hohen Alter 90+)
- Die Sterblichkeitsraten während der Pandemie (2020-2022) waren bei jungen Menschen sogar leicht niedriger
- Im hohen Alter (80-100 Jahre) steigt die Sterbewahrscheinlichkeit exponentiell an

## Dateien im Projekt

### Eingabedaten
- **Sterbetafel2016-2018.csv** - Offizielle deutsche Sterbetafel für die Periode 2016-2018
- **Sterbetafel2020-2022.csv** - Offizielle deutsche Sterbetafel für die Periode 2020-2022
- **Sterbetafel2022-2024.csv** - Offizielle deutsche Sterbetafel für die Periode 2022-2024

### Ausgabedateien

#### Markdown & PDF Reports
- **Sterbevergleich.md** - Markdown-Datei mit allen Tabellen und Daten
- **Sterbevergleich.pdf** - PDF im Landscape-Format (24 KB)
- **Sterbevergleich_2col.pdf** - **Kompaktes 2-spaltiges PDF im Landscape-Format** (16 KB) ⭐

#### Interaktive Visualisierung
- **sterbevergleich_plots.html** - Interaktive Plots mit Plotly.js
  - Plot 1: Alle drei Epochen nebeneinander (nach Geschlecht)
  - Plot 2: Jede Epoche einzeln mit Männer/Frauen/Gesamt-Vergleich
  - Zoom, Pan, Hover-Funktionen für interaktive Exploration
  - Lineare Y-Achse für bessere Vergleichbarkeit

### Python-Skripte

#### Datenverarbeitung
- **Sterbevergleich.py** - Berechnet Sterbewahrscheinlichkeiten für eine CSV-Datei
- **Sterbevergleich_all.py** - Verarbeitet alle 3 CSV-Dateien und generiert Markdown-Report

#### Visualisierung
- **plot_sterbevergleich.py** - Generiert interaktive HTML-Plots mit Plotly
- **generate_pdf.py** - Generiert 2-spaltiges Landscape-PDF

#### Hilfsdateien
- **template.tex** - LaTeX-Template für PDF-Generierung

## Berechnung der Sterbewahrscheinlichkeit

Die Sterbewahrscheinlichkeit für ein Jahrzehnt (z.B. 0-10 Jahre) wird berechnet als:

```
Sterbewahrscheinlichkeit (%) = (l(x) - l(x+10)) / l(x) × 100
```

Wobei:
- `l(x)` = Anzahl der Überlebenden im Alter x (aus Sterbetafel)
- `l(x+10)` = Anzahl der Überlebenden im Alter x+10 (aus Sterbetafel)
- Der Unterschied = Anzahl der Gestorbenen im Jahrzehnt

Beispiel (Männer, 0-10 Jahre, 2016-2018):
```
l(0) = 100.000 Überlebende
l(10) = 99.535 Überlebende
Gestorben = 100.000 - 99.535 = 465
Sterbewahrscheinlichkeit = 465 / 100.000 × 100 = 0.46%
```

## Sterbewahrscheinlichkeit nach Jahrzehnt (Durchschnitt)

| Jahrzehnt | 2016-2018 | 2020-2022 | 2022-2024 | Diff. Pandemie | Diff. Post-Pandemie |
|-----------|-----------|-----------|-----------|----------------|-------------------|
| 0-10 | 0.429% | 0.397% | 0.425% | -7.6% | -1.0% |
| 10-20 | 0.155% | 0.151% | 0.162% | -2.7% | +4.5% |
| 20-30 | 0.325% | 0.317% | 0.331% | -2.4% | +1.9% |
| 30-40 | 0.620% | 0.625% | 0.622% | +0.9% | +0.3% |
| 40-50 | 1.522% | 1.545% | 1.524% | +1.5% | +0.1% |
| 50-60 | 4.389% | 4.242% | 4.073% | -3.4% | -7.2% |
| 60-70 | 10.861% | 11.186% | 10.971% | +3.0% | +1.0% |
| 70-80 | 23.755% | 24.789% | 24.979% | +4.3% | +5.1% |
| 80-90 | 60.739% | 60.561% | 59.915% | -0.3% | -1.4% |
| 90-100 | 95.245% | 95.977% | 95.944% | +0.8% | +0.7% |

## Haupterkenntnis: Kein messbarer Pandemie-Effekt

### Unter 60 Jahren: Kaum Unterschied zu jeder Zeit

**Alle Altersgruppen unter 60 Jahren zeigen minimal unterschiedliche Sterbewahrscheinlichkeiten - sowohl während als auch nach der Pandemie:**

- **0-10 Jahre:** Pandemie -7.6%, Post-Pandemie -1.0%
- **10-20 Jahre:** Pandemie -2.7%, Post-Pandemie +4.5%
- **20-30 Jahre:** Pandemie -2.4%, Post-Pandemie +1.9%
- **30-40 Jahre:** Pandemie +0.9%, Post-Pandemie +0.3%
- **40-50 Jahre:** Pandemie +1.5%, Post-Pandemie +0.1%
- **50-60 Jahre:** Pandemie -3.4%, Post-Pandemie -7.2%

**Die Unterschiede liegen durchgehend unter 8% und sind epidemiologisch nicht signifikant. Die Rückkehr zur Normalität (2022-2024) zeigt keine neuen Trends.**

### Wo stieg die Sterbewahrscheinlichkeit?

**Nur im Alter 60-80 Jahren gab es einen moderaten Anstieg:**

- **60-70 Jahre:** +3.0% während Pandemie, dann +1.0% normalisiert (2022-2024)
- **70-80 Jahre:** +4.3% während Pandemie, fortsetzend +5.1% (2022-2024)
- **Über 80 Jahren:** Praktisch stabil (-0.3% bis +0.8%), keine Erhöhung

Der Anstieg zwischen 60-80 Jahren war moderat und könnte demografische Faktoren (Bevölkerungsalterung) sowie COVID-19-Effekte bei älteren Menschen reflektieren. Jedoch zeigt sich keine dramatische Übersterblichkeit.

### Zusammenfassung

Die Sterbetafeln zeigen **keine dramatische Steigerung der Mortalität**. Die Beobachtungen:
- **Unter 60 Jahren:** Alle Unterschiede unter 8% - epidemiologisch irrelevant
- **60-80 Jahren:** Moderater Anstieg um 3-5%, aber keine Dramatik
- **Über 80 Jahren:** Stabil, trotz hoher absoluter Sterbewahrscheinlichkeit (95%+)
- **Post-Pandemie:** Stabilisierung der Trends, keine Rebound-Effekte

## Verwendung

### 1. Berichte ansehen

```bash
# Markdown-Report lesen
cat Sterbevergleich.md

# PDFs anschauen
open Sterbevergleich.pdf
open Sterbevergleich_2col.pdf  # Empfohlen: kompakt und übersichtlich
```

### 2. Interaktive Plots

```bash
# Browser öffnen mit HTML-Plots
open sterbevergleich_plots.html
```

### 3. Eigene Analysen durchführen

Daten für eine einzelne CSV-Datei berechnen:
```bash
python Sterbevergleich.py
```

Alle 3 Dateien verarbeiten und Markdown generieren:
```bash
python Sterbevergleich_all.py
```

Plots generieren:
```bash
python plot_sterbevergleich.py
```

2-spaltiges PDF generieren:
```bash
python generate_pdf.py
```

## Anforderungen

### Für Python-Skripte
- Python 2.7 oder 3.x
- Keine zusätzlichen Pakete erforderlich

### Für PDF-Generierung
- xelatex (LaTeX-Engine)
- Für pandoc-Konvertierung: pandoc + xelatex

### Für interaktive Plots
- Nur ein Webbrowser erforderlich
- HTML-Datei funktioniert offline (Plotly.js via CDN)

## Datenquellen

- **Quelle:** Statistisches Bundesamt (Destatis), Deutschland
- **Tabelle:** 12621-0001 (Sterbetafeln)
- **Datentyp:** Periodensterbetafeln
- **Geographie:** Deutschland (gesamt)
- **Zeitperioden:**
  - 2016-2018
  - 2020-2022
  - 2022-2024

## Interpretation der Daten

### Sterbewahrscheinlichkeit vs. Sterberate
- **Sterbewahrscheinlichkeit (q(x)):** Wahrscheinlichkeit, dass eine Person zwischen Alter x und x+10 stirbt
- Diese Projekt verwendet q(x)-Werte aus den Sterbetafeln
- Nicht zu verwechseln mit roher Sterberate (Todesfälle pro 1000 Einwohner)

### Lineare Skala in den Plots
- Die interaktiven Plots verwenden eine lineare (nicht logarithmische) Y-Achse
- Dies zeigt die tatsächliche Magnitude der Sterblichkeit
- Im hohen Alter dominiert die exponentielle Zunahme die Visualisierung

## Struktur der Sterbetafel-CSV

Jede CSV-Datei enthält für jedes Alter (0-100+ Jahre):
- **Alter:** Vollendetes Alter (z.B. "0 Jahre", "10 Jahre")
- **q(x):** Sterbewahrscheinlichkeit
- **p(x):** Überlebenswahrscheinlichkeit
- **l(x):** Überlebende (auf 100.000 normalisiert)
- **d(x):** Gestorbene
- **L(x):** Durchlebte Jahre
- **T(x):** Restlebenserwartung
- **e(x):** Durchschnittliche Lebenserwartung

Daten sind separat für Männer und Frauen vorhanden.

## Lizenz

Daten: Statistisches Bundesamt (Destatis) - Public Domain

Skripte und Analyse: Ohne Lizenzangabe

## Fragen & Support

Für Fragen zur Datenbeschaffung oder Sterbetafeln:
- Kontaktieren Sie das Statistische Bundesamt: https://www.destatis.de/

Für Fragen zu diesem Projekt:
- Siehe GitHub Issues oder Dokumentation

## Changelog

### v1.0 (09.12.2025)
- Initial version
- Analyse der 3 Sterbetafeln (2016-2018, 2020-2022, 2022-2024)
- Markdown-Report mit vergleichenden Tabellen
- Interaktive HTML-Plots
- PDF-Reports (einspaltig und 2-spaltig)
- Alle Python-Skripte zur Datenverarbeitung
