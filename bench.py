#!/usr/bin/env python

import sys, os, subprocess, signal

import bench_common

count_multipliers = {
    'append_': 100, # append is generally very fast
    'prepend_': 1,
    'insert1_mid_': 1,
    'insert1_quarter_': 1,
    'insert1_last_quarter_': 1,
    'access_every_': 100, # accessing is also very fast
    'remove_first_': 1,
    'remove_mid_': 1,
    'remove_last_': 100,
}

def find_op(benchtype):
    for op in bench_common.ops:
        if benchtype.startswith(op):
            return op
    return None

# basic benchmark from 20k to 100k elements
minkeys  =  2*10*1000
maxkeys  = 10*10*1000
interval =  2*10*1000
best_out_of = 7

outfile = open('output', 'w')

if len(sys.argv) > 1:
    benchtypes = sys.argv[1:]
else:

    benchtypes = []
    for suffix in ["int", "qstr", "stdstr", "three_ptrs"]:
        benchtypes = benchtypes + [op + suffix for op in bench_common.ops]

for nkeys in range(minkeys, maxkeys + 1, interval):
    for benchtype in benchtypes:
        # adjust number of iterations based on operation type
        adjusted_nkeys = nkeys * count_multipliers[find_op(benchtype)]

        for program in bench_common.programs:
            if program.startswith('tsl_array_map') and 'string' not in benchtype:
                continue


            fastest_attempt = 1000000
            fastest_attempt_data = ''

            for attempt in range(best_out_of):
                try:
                    output = subprocess.check_output(['./build/' + program, str(adjusted_nkeys), benchtype])
                    words = output.strip().split()

                    runtime_seconds = float(words[0])
                    memory_usage_bytes = int(words[1])
                    load_factor = float(words[2])
                except:
                    print("Error with %s" % str(['./build/' + program, str(adjusted_nkeys), benchtype]))
                    break

                line = ','.join(map(str, [benchtype, adjusted_nkeys, program, "%0.2f" % load_factor,
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
