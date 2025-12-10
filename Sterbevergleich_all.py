# -*- coding: utf-8 -*-
import os

def process_csv_file(csv_file):
    """Verarbeitet eine CSV-Datei und gibt die Sterbewahrscheinlichkeiten pro Jahrzehnt zurück"""
    with open(csv_file, 'rb') as f:
        content = f.read()
        try:
            text = content.decode('utf-8-sig')
        except UnicodeDecodeError:
            text = content.decode('latin-1')

        lines = text.splitlines()

    def clean_number(value_str):
        """Extrahiert die Zahl aus einem String mit 'e'-Suffix"""
        try:
            cleaned = value_str.strip().rstrip('e').strip()
            cleaned = cleaned.replace(',', '.')
            return float(cleaned)
        except:
            return None

    survivors = {}

    # Verarbeite alle Datenzeilen
    for line in lines:
        if not line.strip() or 'Jahre' not in line or not line[0].isdigit():
            continue

        parts = line.split(';')
        if len(parts) < 20:
            continue

        age_str = parts[0].strip().split()[0]
        try:
            age = int(age_str)
        except:
            continue

        # Spalte 5: l(x) Männer, Spalte 19: l(x) Frauen
        male_survivors = clean_number(parts[5])
        female_survivors = clean_number(parts[19])

        if male_survivors is not None and female_survivors is not None:
            survivors[age] = {
                'männlich': male_survivors,
                'weiblich': female_survivors
            }

    # Jahrzehnte berechnen
    results = {}
    for start_age in range(0, 100, 5): # Adjusted range for 5-year intervals
        end_age = start_age + 5 # Adjusted end_age for 5-year intervals

        if start_age in survivors and end_age in survivors:
            l_start_male = survivors[start_age]['männlich']
            l_start_female = survivors[start_age]['weiblich']
            l_end_male = survivors[end_age]['männlich']
            l_end_female = survivors[end_age]['weiblich']

            prob_death_male = ((l_start_male - l_end_male) / l_start_male) * 100
            prob_death_female = ((l_start_female - l_end_female) / l_start_female) * 100
            # Durchschnitt statt Addition, da die Werte normalisiert sind
            prob_death_total = (prob_death_male + prob_death_female) / 2.0

            results["{}-{}".format(start_age, end_age)] = { # Key will now be like "0-4", "5-9", etc.
                'männlich': prob_death_male,
                'weiblich': prob_death_female,
                'zusammen': prob_death_total
            }

    return results


# Verarbeite alle drei CSV-Dateien
base_dir = '/Users/haraldbeker/PythonProjects/Sterbetafeln'
csv_files = {
    '2016-2018': os.path.join(base_dir, 'Sterbetafel2016-2018.csv'),
    '2020-2022': os.path.join(base_dir, 'Sterbetafel2020-2022.csv'),
    '2022-2024': os.path.join(base_dir, 'Sterbetafel2022-2024.csv')
}

results_all = {}
for period, csv_file in csv_files.items():
    results_all[period] = process_csv_file(csv_file)

# Generiere Markdown-Datei
md_lines = []
md_lines.append(b"# Sterbevergleich - Deutsche Sterbetafeln")
md_lines.append(b"")
md_lines.append(b"Sterbewahrscheinlichkeiten pro Jahrzehnt fur die Perioden 2016-2018, 2020-2022 und 2022-2024")
md_lines.append(b"")

# Gesamtübersicht Männer
md_lines.append(b"## Maenner - Sterbewahrscheinlichkeit (%)")
md_lines.append(b"")
md_lines.append(b"| Jahrzehnt | 2016-2018 | 2020-2022 | % Aenderung | 2022-2024 | % Aenderung |")
md_lines.append(b"|-----------|-----------|-----------|-------------|-----------|-------------|")
for decade in sorted(results_all['2016-2018'].keys(), key=lambda x: int(x.split('-')[0])):
    values = [decade]
    if decade in results_all['2016-2018']:
        baseline = results_all['2016-2018'][decade]['männlich']
        values.append("{:.4f}".format(baseline))

        # 2020-2022 comparison
        if decade in results_all['2020-2022']:
            val_2022 = results_all['2020-2022'][decade]['männlich']
            values.append("{:.4f}".format(val_2022))
            if baseline != 0:
                pct_change_2022 = ((val_2022 - baseline) / baseline) * 100
                values.append("{:+.2f}%".format(pct_change_2022))
            else:
                values.append("N/A")
        else:
            values.append("-")
            values.append("-")

        # 2022-2024 comparison
        if decade in results_all['2022-2024']:
            val_2024 = results_all['2022-2024'][decade]['männlich']
            values.append("{:.4f}".format(val_2024))
            if baseline != 0:
                pct_change_2024 = ((val_2024 - baseline) / baseline) * 100
                values.append("{:+.2f}%".format(pct_change_2024))
            else:
                values.append("N/A")
        else:
            values.append("-")
            values.append("-")

    line = "| {} |".format(" | ".join(values))
    md_lines.append(line.encode('utf-8'))
md_lines.append(b"")

# Gesamtübersicht Frauen
md_lines.append(b"## Frauen - Sterbewahrscheinlichkeit (%)")
md_lines.append(b"")
md_lines.append(b"| Jahrzehnt | 2016-2018 | 2020-2022 | % Aenderung | 2022-2024 | % Aenderung |")
md_lines.append(b"|-----------|-----------|-----------|-------------|-----------|-------------|")
for decade in sorted(results_all['2016-2018'].keys(), key=lambda x: int(x.split('-')[0])):
    values = [decade]
    if decade in results_all['2016-2018']:
        baseline = results_all['2016-2018'][decade]['weiblich']
        values.append("{:.4f}".format(baseline))

        # 2020-2022 comparison
        if decade in results_all['2020-2022']:
            val_2022 = results_all['2020-2022'][decade]['weiblich']
            values.append("{:.4f}".format(val_2022))
            if baseline != 0:
                pct_change_2022 = ((val_2022 - baseline) / baseline) * 100
                values.append("{:+.2f}%".format(pct_change_2022))
            else:
                values.append("N/A")
        else:
            values.append("-")
            values.append("-")

        # 2022-2024 comparison
        if decade in results_all['2022-2024']:
            val_2024 = results_all['2022-2024'][decade]['weiblich']
            values.append("{:.4f}".format(val_2024))
            if baseline != 0:
                pct_change_2024 = ((val_2024 - baseline) / baseline) * 100
                values.append("{:+.2f}%".format(pct_change_2024))
            else:
                values.append("N/A")
        else:
            values.append("-")
            values.append("-")

    line = "| {} |".format(" | ".join(values))
    md_lines.append(line.encode('utf-8'))
md_lines.append(b"")

# Gesamtübersicht Männer + Frauen
md_lines.append(b"## Zusammen (Maenner + Frauen) - Sterbewahrscheinlichkeit (%)")
md_lines.append(b"")
md_lines.append(b"| Jahrzehnt | 2016-2018 | 2020-2022 | % Aenderung | 2022-2024 | % Aenderung |")
md_lines.append(b"|-----------|-----------|-----------|-------------|-----------|-------------|")
for decade in sorted(results_all['2016-2018'].keys(), key=lambda x: int(x.split('-')[0])):
    values = [decade]
    if decade in results_all['2016-2018']:
        baseline = results_all['2016-2018'][decade]['zusammen']
        values.append("{:.4f}".format(baseline))

        # 2020-2022 comparison
        if decade in results_all['2020-2022']:
            val_2022 = results_all['2020-2022'][decade]['zusammen']
            values.append("{:.4f}".format(val_2022))
            if baseline != 0:
                pct_change_2022 = ((val_2022 - baseline) / baseline) * 100
                values.append("{:+.2f}%".format(pct_change_2022))
            else:
                values.append("N/A")
        else:
            values.append("-")
            values.append("-")

        # 2022-2024 comparison
        if decade in results_all['2022-2024']:
            val_2024 = results_all['2022-2024'][decade]['zusammen']
            values.append("{:.4f}".format(val_2024))
            if baseline != 0:
                pct_change_2024 = ((val_2024 - baseline) / baseline) * 100
                values.append("{:+.2f}%".format(pct_change_2024))
            else:
                values.append("N/A")
        else:
            values.append("-")
            values.append("-")

    line = "| {} |".format(" | ".join(values))
    md_lines.append(line.encode('utf-8'))
md_lines.append(b"")

# Detaillierte Analyse pro Periode
for period in ['2016-2018', '2020-2022', '2022-2024']:
    md_lines.append("## Detaillierte Analyse - Periode {}".format(period).encode('utf-8'))
    md_lines.append(b"")

    for decade in sorted(results_all[period].keys(), key=lambda x: int(x.split('-')[0])):
        result = results_all[period][decade]
        start_age, end_age = decade.split('-')

        md_lines.append("### Jahrzehnt {}-{} Jahre".format(start_age, end_age).encode('utf-8'))
        md_lines.append(b"")
        md_lines.append(b"| Kategorie | Sterbewahrscheinlichkeit |")
        md_lines.append(b"|-----------|--------------------------|")
        md_lines.append("| Maenner | {:.2f}% |".format(result['männlich']).encode('utf-8'))
        md_lines.append("| Frauen | {:.2f}% |".format(result['weiblich']).encode('utf-8'))
        md_lines.append("| Zusammen | {:.2f}% |".format(result['zusammen']).encode('utf-8'))
        md_lines.append(b"")

# Schreibe in Markdown-Datei
output_file = os.path.join(base_dir, 'Sterbevergleich.md')
with open(output_file, 'wb') as f:
    f.write(b'\n'.join(md_lines))

print("Markdown-Datei erfolgreich erstellt: {}".format(output_file))
