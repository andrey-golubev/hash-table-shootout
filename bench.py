#!/usr/bin/env python

import sys, os, subprocess, signal

programs = [
    'std_vector',
    'std_vector515',
    'qlist_qt6',
    'qlist_qt515',
    'qvector_qt515',
]

minkeys  =  2*100*1000
maxkeys  = 10*100*1000
interval =  2*100*1000
best_out_of = 5

outfile = open('output', 'w')

if len(sys.argv) > 1:
    benchtypes = sys.argv[1:]
else:
    ops = [
        'append_',
        'prepend_',
        'insert1_mid_',
        'insert1_quarter_',
        'insert1_last_quarter_',
        'access_every_',
        'remove_first_',
        'remove_mid_',
        'remove_last_',
    ]
    benchtypes = []
    for suffix in ["int", "qstr", "stdstr", "three_ptrs"]:
        benchtypes = benchtypes + [op + suffix for op in ops]

for nkeys in range(minkeys, maxkeys + 1, interval):
    for benchtype in benchtypes:
        for program in programs:
            if program.startswith('tsl_array_map') and 'string' not in benchtype:
                continue

            fastest_attempt = 1000000
            fastest_attempt_data = ''

            for attempt in range(best_out_of):
                try:
                    output = subprocess.check_output(['./build/' + program, str(nkeys), benchtype])
                    words = output.strip().split()

                    runtime_seconds = float(words[0])
                    memory_usage_bytes = int(words[1])
                    load_factor = float(words[2])
                except:
                    print("Error with %s" % str(['./build/' + program, str(nkeys), benchtype]))
                    break

                line = ','.join(map(str, [benchtype, nkeys, program, "%0.2f" % load_factor,
                                          memory_usage_bytes, "%0.6f" % runtime_seconds]))

                if runtime_seconds < fastest_attempt:
                    fastest_attempt = runtime_seconds
                    fastest_attempt_data = line

            if fastest_attempt != 1000000:
                print >> outfile, fastest_attempt_data
                print fastest_attempt_data

        # Print blank line
        print >> outfile
        print
