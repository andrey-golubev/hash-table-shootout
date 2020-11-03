#!/usr/bin/env python

import sys

op2html = {
    'append_': '<h3>Append one element: execution time</h3></br><p>Appending into container, without prior space reservation.</p></br>',
    'prepend_': '<h3>Prepend one element: execution time</h3></br><p>Prepending into container, without prior space reservation.</p></br>',
    'insert1_mid_': '<h3>Insert one element in the middle: execution time</h3></br><p>Inserting into container, without prior space reservation.</p></br>',
    'insert1_quarter_': '<h3>Insert one element in the first quarter (e.g. pos = size() / 4): execution time</h3></br><p>Inserting into container, without prior space reservation.</p></br>',
    'insert1_last_quarter_': '<h3>Insert one element in the last quarter (e.g. pos = 3 * size() / 4): execution time</h3></br><p>Inserting into container, without prior space reservation.</p></br>',
    'access_every_': '<h3>Accessing every element: execution time</h3></br><p>Resize container to specified size, then access each element.</p></br>',
    'remove_first_': '<h3>Remove first element: execution time</h3></br><p>Resize container to specified size, remove first element in a loop.</p></br>',
    'remove_mid_': '<h3>Remove middle element: execution time</h3></br><p>Resize container to specified size, remove middle element in a loop.</p></br>',
    'remove_last_': '<h3>Remove last element: execution time</h3></br><p>Resize container to specified size, remove last element in a loop.</p></br>',
}

suffix2pos = {
    'int': '__TEST_DATA_INT_GOES_HERE__',
    'qstr': '__TEST_DATA_QSTR_GOES_HERE__',
    'stdstr': '__TEST_DATA_STDSTR_GOES_HERE__',
    'three_ptrs': '__TEST_DATA_THREE_PTRS_GOES_HERE__',
}

def construct_table(suffix, op):
    heading = op2html[op]
    identifier = op + suffix
    chart = '<div class="chart" id="%s"></div>' % identifier
    title = '<div class="xaxis-title">number of entries in container</div>'
    checkboxes = '<ul class="choices" id="%s_choices"></ul>' % identifier
    return '\n'.join([heading, '</br>', '\n'.join([chart, title, checkboxes]), '</br>'])

def insert_bench_layout(html_template):
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

    for suffix in ["int", "qstr", "stdstr", "three_ptrs"]:
        # construct full table
        full_table = []
        for op in ops:
            minitable = construct_table(suffix, op)
            full_table.append(minitable)
        html_template = html_template.replace(suffix2pos[suffix], '\n</br>\n'.join(full_table))

    return html_template

html_template = file('charts-template.html', 'r').read()
html_template = insert_bench_layout(html_template)
file('charts.html', 'w').write(html_template.replace('__CHART_DATA_GOES_HERE__', sys.stdin.read()))
