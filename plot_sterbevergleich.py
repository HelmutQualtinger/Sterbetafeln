# -*- coding: utf-8 -*-
import os
import json

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
        try:
            cleaned = value_str.strip().rstrip('e').strip()
            cleaned = cleaned.replace(',', '.')
            return float(cleaned)
        except:
            return None

    survivors = {}

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

        male_survivors = clean_number(parts[5])
        female_survivors = clean_number(parts[19])

        if male_survivors is not None and female_survivors is not None:
            survivors[age] = {
                'männlich': male_survivors,
                'weiblich': female_survivors
            }

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
            prob_death_total = (prob_death_male + prob_death_female) / 2.0

            results["{}-{}".format(start_age, end_age)] = { # Key will now be like "0-4", "5-9", etc.
                'männlich': prob_death_male,
                'weiblich': prob_death_female,
                'zusammen': prob_death_total
            }
    return results


base_dir = '/Users/haraldbeker/PythonProjects/Sterbetafeln'
csv_files = {
    '2016-2018': os.path.join(base_dir, 'Sterbetafel2016-2018.csv'),
    '2020-2022': os.path.join(base_dir, 'Sterbetafel2020-2022.csv'),
    '2022-2024': os.path.join(base_dir, 'Sterbetafel2022-2024.csv')
}

results_all = {}
for period, csv_file in csv_files.items():
    results_all[period] = process_csv_file(csv_file)

# Fetching keys from the first period's results for consistent ordering and labels
period_keys = list(results_all['2016-2018'].keys())
# Ensure keys are sorted correctly for plotting (e.g., "0-4", "5-9", "10-14", ...)
# Simple alphabetical sort might work for "0-4", "10-14", "5-9" etc. if numbers are zero-padded,
# but a custom sort based on the start age would be more robust.
# For now, assuming the keys are generated in a sortable order or can be directly used.
ages = sorted(period_keys, key=lambda x: int(x.split('-')[0])) # Sort by the start of the interval

# Preparation of data
data_male = {period: [results_all[period][age_label]['männlich'] for age_label in ages] for period in csv_files.keys()}
data_female = {period: [results_all[period][age_label]['weiblich'] for age_label in ages] for period in csv_files.keys()}
data_total = {period: [results_all[period][age_label]['zusammen'] for age_label in ages] for period in csv_files.keys()}

# Konvertiere Keys für JSON (da "männlich" etc. im JSON sein müssen)
json_data_male = json.dumps(data_male, ensure_ascii=False)
json_data_female = json.dumps(data_female, ensure_ascii=False)
json_data_total = json.dumps(data_total, ensure_ascii=False)
json_ages = json.dumps(ages) # This will be the list of interval labels like "0-4", "5-9"

# HTML-Template
html_template = u'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Sterbevergleich - Interaktive Plots</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1, h2 {{
            color: #333;
        }}
        .plot {{
            width: 100%;
            height: 600px;
        }}
        .plot-row {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}
        @media (max-width: 1400px) {{
            .plot-row {{
                grid-template-columns: 1fr;
            }}
        }}
        .info {{
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #1976d2;
            margin: 20px 0;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <h1>Sterbewahrscheinlichkeit - Vergleich deutscher Sterbetafeln</h1>

    <div class="info">
        <strong>Datenquelle:</strong> Deutsche Sterbetafeln 2016-2018, 2020-2022, 2022-2024<br>
        <strong>Darstellung:</strong> Lineare Skala
    </div>

    <h2>Plot 1: Alle drei Epochen nebeneinander (nach Geschlecht)</h2>

    <div class="plot-row">
        <div id="plot1-male" class="plot"></div>
        <div id="plot1-female" class="plot"></div>
        <div id="plot1-total" class="plot"></div>
    </div>

    <h2>Plot 2: Jede Epoche einzeln (Männer, Frauen, Gesamt)</h2>

    <div class="plot-row">
        <div id="plot2-2016" class="plot"></div>
        <div id="plot2-2020" class="plot"></div>
        <div id="plot2-2022" class="plot"></div>
    </div>

    <script>
        var ages = {ages};
        var data_male = {data_male};
        var data_female = {data_female};
        var data_total = {data_total};

        var colors = {{
            '2016-2018': '#1f77b4',
            '2020-2022': '#ff7f0e',
            '2022-2024': '#2ca02c'
        }};

        // Plot 1: Männer
        var trace1_male_2016 = {{x: ages, y: data_male['2016-2018'], mode: 'lines+markers', name: '2016-2018', line: {{color: colors['2016-2018']}}, marker: {{size: 6}}}};
        var trace1_male_2020 = {{x: ages, y: data_male['2020-2022'], mode: 'lines+markers', name: '2020-2022', line: {{color: colors['2020-2022']}}, marker: {{size: 6}}}};
        var trace1_male_2022 = {{x: ages, y: data_male['2022-2024'], mode: 'lines+markers', name: '2022-2024', line: {{color: colors['2022-2024']}}, marker: {{size: 6}}}};
        var layout1_male = {{title: 'Männer', xaxis: {{title: 'Alter (Jahre)'}}, yaxis: {{title: 'Sterbewahrscheinlichkeit (%)'}}, hovermode: 'x unified'}};
        Plotly.newPlot('plot1-male', [trace1_male_2016, trace1_male_2020, trace1_male_2022], layout1_male, {{responsive: true}});

        // Plot 1: Frauen
        var trace1_female_2016 = {{x: ages, y: data_female['2016-2018'], mode: 'lines+markers', name: '2016-2018', line: {{color: colors['2016-2018']}}, marker: {{size: 6}}}};
        var trace1_female_2020 = {{x: ages, y: data_female['2020-2022'], mode: 'lines+markers', name: '2020-2022', line: {{color: colors['2020-2022']}}, marker: {{size: 6}}}};
        var trace1_female_2022 = {{x: ages, y: data_female['2022-2024'], mode: 'lines+markers', name: '2022-2024', line: {{color: colors['2022-2024']}}, marker: {{size: 6}}}};
        var layout1_female = {{title: 'Frauen', xaxis: {{title: 'Alter (Jahre)'}}, yaxis: {{title: 'Sterbewahrscheinlichkeit (%)'}}, hovermode: 'x unified'}};
        Plotly.newPlot('plot1-female', [trace1_female_2016, trace1_female_2020, trace1_female_2022], layout1_female, {{responsive: true}});

        // Plot 1: Gesamt
        var trace1_total_2016 = {{x: ages, y: data_total['2016-2018'], mode: 'lines+markers', name: '2016-2018', line: {{color: colors['2016-2018']}}, marker: {{size: 6}}}};
        var trace1_total_2020 = {{x: ages, y: data_total['2020-2022'], mode: 'lines+markers', name: '2020-2022', line: {{color: colors['2020-2022']}}, marker: {{size: 6}}}};
        var trace1_total_2022 = {{x: ages, y: data_total['2022-2024'], mode: 'lines+markers', name: '2022-2024', line: {{color: colors['2022-2024']}}, marker: {{size: 6}}}};
        var layout1_total = {{title: 'Gesamt (Durchschnitt)', xaxis: {{title: 'Alter (Jahre)'}}, yaxis: {{title: 'Sterbewahrscheinlichkeit (%)'}}, hovermode: 'x unified'}};
        Plotly.newPlot('plot1-total', [trace1_total_2016, trace1_total_2020, trace1_total_2022], layout1_total, {{responsive: true}});

        // Plot 2: Periode 2016-2018
        var trace2_2016_m = {{x: ages, y: data_male['2016-2018'], mode: 'lines+markers', name: 'Männer', line: {{color: '#1f77b4'}}, marker: {{size: 6}}}};
        var trace2_2016_w = {{x: ages, y: data_female['2016-2018'], mode: 'lines+markers', name: 'Frauen', line: {{color: '#ff1493'}}, marker: {{size: 6}}}};
        var trace2_2016_t = {{x: ages, y: data_total['2016-2018'], mode: 'lines+markers', name: 'Gesamt', line: {{color: '#2ca02c'}}, marker: {{size: 6}}}};
        var layout2_2016 = {{title: 'Periode 2016-2018', xaxis: {{title: 'Alter (Jahre)'}}, yaxis: {{title: 'Sterbewahrscheinlichkeit (%)'}}, hovermode: 'x unified'}};
        Plotly.newPlot('plot2-2016', [trace2_2016_m, trace2_2016_w, trace2_2016_t], layout2_2016, {{responsive: true}});

        // Plot 2: Periode 2020-2022
        var trace2_2020_m = {{x: ages, y: data_male['2020-2022'], mode: 'lines+markers', name: 'Männer', line: {{color: '#1f77b4'}}, marker: {{size: 6}}}};
        var trace2_2020_w = {{x: ages, y: data_female['2020-2022'], mode: 'lines+markers', name: 'Frauen', line: {{color: '#ff1493'}}, marker: {{size: 6}}}};
        var trace2_2020_t = {{x: ages, y: data_total['2020-2022'], mode: 'lines+markers', name: 'Gesamt', line: {{color: '#2ca02c'}}, marker: {{size: 6}}}};
        var layout2_2020 = {{title: 'Periode 2020-2022 (Pandemie)', xaxis: {{title: 'Alter (Jahre)'}}, yaxis: {{title: 'Sterbewahrscheinlichkeit (%)'}}, hovermode: 'x unified'}};
        Plotly.newPlot('plot2-2020', [trace2_2020_m, trace2_2020_w, trace2_2020_t], layout2_2020, {{responsive: true}});

        // Plot 2: Periode 2022-2024
        var trace2_2022_m = {{x: ages, y: data_male['2022-2024'], mode: 'lines+markers', name: 'Männer', line: {{color: '#1f77b4'}}, marker: {{size: 6}}}};
        var trace2_2022_w = {{x: ages, y: data_female['2022-2024'], mode: 'lines+markers', name: 'Frauen', line: {{color: '#ff1493'}}, marker: {{size: 6}}}};
        var trace2_2022_t = {{x: ages, y: data_total['2022-2024'], mode: 'lines+markers', name: 'Gesamt', line: {{color: '#2ca02c'}}, marker: {{size: 6}}}};
        var layout2_2022 = {{title: 'Periode 2022-2024', xaxis: {{title: 'Alter (Jahre)'}}, yaxis: {{title: 'Sterbewahrscheinlichkeit (%)'}}, hovermode: 'x unified'}};
        Plotly.newPlot('plot2-2022', [trace2_2022_m, trace2_2022_w, trace2_2022_t], layout2_2022, {{responsive: true}});
    </script>
</body>
</html>
'''

html_content = html_template.format(
    ages=json_ages,
    data_male=json_data_male,
    data_female=json_data_female,
    data_total=json_data_total
)

output_file = os.path.join(base_dir, 'sterbevergleich_plots.html')
with open(output_file, 'wb') as f:
    f.write(html_content.encode('utf-8'))

print("HTML-Plot-Datei erstellt: {}".format(output_file))
