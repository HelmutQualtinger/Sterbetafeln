# -*- coding: utf-8 -*-
import csv
import os

# Pfad zur CSV-Datei
csv_file = os.path.join(os.path.dirname(__file__), 'Sterbetafel2016-2018.csv')

# CSV-Datei mit Semicolon-Trennzeichen einlesen
data = []
with open(csv_file, 'rb') as f:
    content = f.read()
    try:
        text = content.decode('utf-8-sig')
    except UnicodeDecodeError:
        text = content.decode('latin-1')

    lines = text.splitlines()
    for line in lines:
        # Manuelles Splitten auf Semicolon
        row = line.split(';')
        data.append(row)

# Die Header-Zeilen überspringen und die Daten ab Zeile 11 (Index 10) verarbeiten
# Spalte 5 (Index 5): Überlebende Männer [l(x)]
# Spalte 19 (Index 19): Überlebende Frauen [l(x)]
# Spalte 0: Alter

def extract_age(age_str):
    """Extrahiert die numerische Alter aus dem String (z.B. '0 Jahre' -> 0)"""
    try:
        return int(age_str.split()[0])
    except:
        return None

def extract_number(value_str):
    """Extrahiert die Zahl aus einem String, der möglicherweise mit 'e' endet"""
    try:
        # Entfernt 'e' am Ende wenn vorhanden
        cleaned = value_str.strip().rstrip('e').strip()
        # Deutsche Zahlenformat (Komma statt Punkt)
        cleaned = cleaned.replace(',', '.')
        return float(cleaned)
    except:
        return None

# Daten sammeln: {alter: {geschlecht: überlebende}}
survivors = {}

for i, row in enumerate(data):
    if i < 10:  # Header überspringen
        continue

    if len(row) < 20:  # Ungültige Zeile
        continue

    age_str = row[0].strip()
    if not age_str or age_str == '2016/18':
        continue

    age = extract_age(age_str)
    if age is None:
        continue

    # Überlebende extrahieren
    male_survivors = extract_number(row[5])
    female_survivors = extract_number(row[19])

    if male_survivors is not None and female_survivors is not None:
        survivors[age] = {
            'männlich': male_survivors,
            'weiblich': female_survivors
        }

# Jahrzehnte berechnen (0-10, 10-20, ..., 90-100)
decades = []
for start_age in range(0, 100, 5): # Adjusted range for 5-year intervals
    end_age = start_age + 5 # Adjusted end_age for 5-year intervals

    if start_age in survivors and end_age in survivors:
        decades.append((start_age, end_age))

print("=" * 80)
print("STERBEVERGLEICH - Sterbewahrscheinlichkeiten pro Jahrzehnt")
print("Datenquelle: Sterbetafel 2016-2018 (Deutschland)")
print("=" * 80)
print("")

# Tabellenkopf
header = "Jahrzehnt       Männer (%)      Frauen (%)      Zusammen (%)"
print(header)
print("-" * 60)

# Ergebnisse berechnen und ausgeben
for start_age, end_age in decades:
    # Überlebende am Anfang des Jahrzehnts
    l_start_male = survivors[start_age]['männlich']
    l_start_female = survivors[start_age]['weiblich']
    l_start_total = l_start_male + l_start_female

    # Überlebende am Ende des Jahrzehnts
    l_end_male = survivors[end_age]['männlich']
    l_end_female = survivors[end_age]['weiblich']
    l_end_total = l_start_total - (l_start_male - l_end_male) - (l_start_female - l_end_female)

    # Sterbewahrscheinlichkeit = (l(x) - l(x+10)) / l(x)
    prob_death_male = ((l_start_male - l_end_male) / l_start_male) * 100
    prob_death_female = ((l_start_female - l_end_female) / l_start_female) * 100
    prob_death_total = ((l_start_total - l_end_total) / l_start_total) * 100

    decade_label = "{}-{} Jahre".format(start_age, end_age)
    line = "{:<15} {:<15.4f} {:<15.4f} {:<15.4f}".format(decade_label, prob_death_male, prob_death_female, prob_death_total)
    print(line)

print("-" * 60)
print("")

# Detaillierte Ausgabe
print("=" * 80)
print("DETAILLIERTE ANALYSE")
print("=" * 80)
print("")

for start_age, end_age in decades:
    l_start_male = survivors[start_age]['männlich']
    l_start_female = survivors[start_age]['weiblich']
    l_end_male = survivors[end_age]['männlich']
    l_end_female = survivors[end_age]['weiblich']

    prob_death_male = ((l_start_male - l_end_male) / l_start_male) * 100
    prob_death_female = ((l_start_female - l_end_female) / l_start_female) * 100
    prob_death_total = ((l_start_male + l_start_female - l_end_male - l_end_female) / (l_start_male + l_start_female)) * 100

    print("Jahrzehnt {}-{} Jahre:".format(start_age, end_age))
    print("  Männer:")
    print("    - Überlebende am Anfang: {}".format(int(l_start_male)).rjust(8))
    print("    - Überlebende am Ende:   {}".format(int(l_end_male)).rjust(8))
    print("    - Gestorben:             {}".format(int(l_start_male - l_end_male)).rjust(8))
    print("    - Sterbewahrscheinlichkeit: {:.2f}%".format(prob_death_male))
    print("")
    print("  Frauen:")
    print("    - Überlebende am Anfang: {}".format(int(l_start_female)).rjust(8))
    print("    - Überlebende am Ende:   {}".format(int(l_end_female)).rjust(8))
    print("    - Gestorben:             {}".format(int(l_start_female - l_end_female)).rjust(8))
    print("    - Sterbewahrscheinlichkeit: {:.2f}%".format(prob_death_female))
    print("")
    print("  Zusammen (Männer + Frauen):")
    print("    - Überlebende am Anfang: {}".format(int(l_start_male + l_start_female)).rjust(8))
    print("    - Überlebende am Ende:   {}".format(int(l_end_male + l_end_female)).rjust(8))
    print("    - Gestorben:             {}".format(int(l_start_male + l_start_female - l_end_male - l_end_female)).rjust(8))
    print("    - Sterbewahrscheinlichkeit: {:.2f}%".format(prob_death_total))
    print("")
    print("-" * 80)
    print("")