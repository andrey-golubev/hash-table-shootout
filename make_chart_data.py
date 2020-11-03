#!/usr/bin/env python

import sys, json
from collections import OrderedDict

lines = [ line.strip() for line in sys.stdin if line.strip() ]

by_benchtype = {}

for line in lines:
    benchtype, nkeys, program, load_factor, nbytes, runtime = line.split(',')
    nkeys = int(nkeys)
    nbytes = int(nbytes)
    runtime = float(runtime)
    load_factor = float(load_factor)

    by_benchtype.setdefault("%s_runtime" % benchtype, {}).setdefault(program, []).append([nkeys, runtime, load_factor])
    by_benchtype.setdefault("%s_memory"  % benchtype, {}).setdefault(program, []).append([nkeys, nbytes, load_factor])

proper_names = OrderedDict([
    ('std_vector', 'std::vector'),
    ('std_vector515', 'std::vector (with Qt 5.15)'),
    ('qlist_qt6', 'QList (dev)'),
    ('qlist_qt515', 'QList (5.15)'),
    ('qvector_qt515', 'QVector (5.15)'),
])

# do them in the desired order to make the legend not overlap the chart data
# too much
program_slugs = [
    'std_vector',
    'qlist_qt6',
    'qlist_qt515',
    'qvector_qt515',
    'std_vector515',
]

# programs which will be shown (checkbox checked)
default_programs_show = [
    'std_vector',
    'std_vector515',
    'qlist_qt6',
    'qlist_qt515',
    'qvector_qt515',
]

chart_data = {}

for i, (benchtype, programs) in enumerate(by_benchtype.items()):
    chart_data[benchtype] = []
    for j, program in enumerate(program_slugs):
        if program not in programs:
            continue

        data = programs[program]
        chart_data[benchtype].append({
            'program': program,
            'label': proper_names[program],
            'data': [],
        })

        for k, (nkeys, value, load_factor) in enumerate(data):
            chart_data[benchtype][-1]['data'].append([nkeys, value, load_factor])

json_text = json.dumps(chart_data)
json_text = json_text.replace("}], ", "}], \n")
print('chart_data = ' + json_text + ';')
print('\nprograms = ' + json.dumps(proper_names, indent=1) + ';')
print('\ndefault_programs_show = ' + str(default_programs_show) + ';')
