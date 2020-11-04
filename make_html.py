#!/usr/bin/env python

import sys

import bench_common

suffixes = [
    'int',
    'qstr',
    'stdstr',
    'three_ptrs',
]

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
    'remove_first_special_': '<h3>Remove first element (special case): execution time</h3></br><p>Resize container to specified size, remove first element in a loop, calling removeFirst() for Qt containers.</p></br>',
    'remove_last_special_': '<h3>Remove last element (special case): execution time</h3></br><p>Resize container to specified size, remove last element in a loop, calling removeLast() for Qt containers.</p></br>',
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

def insert_charts(html_template):
    # group by type:
    for suffix in suffixes:
        # construct full table
        full_table = []
        for op in bench_common.ops:
            minitable = construct_table(suffix, op)
            full_table.append(minitable)
        html_template = html_template.replace(suffix2pos[suffix], '\n</br>\n'.join(full_table))

    return html_template

def construct_js_line_runtime(suffix, op):
    identifier = op + suffix
    js_line = "        plot_chart(chart_data['%s_runtime'], '#%s', '#%s_choices', runtime_settings, redraw_only);" % (identifier, identifier, identifier)
    return js_line


def insert_plot_data_logic(html_template):
    full_js_script = []
    # group by operation:
    for op in bench_common.ops:
        full_js_script.append("        // operation - %s*" % op)
        for suffix in suffixes:
            full_js_script.append(construct_js_line_runtime(suffix, op))
        full_js_script.append('\n')
    return html_template.replace('__PLOT_FUNC_RUNTIME_DATA_GOES_HERE__', '\n'.join(full_js_script))

html_template = file('charts-template.html', 'r').read()
html_template = insert_charts(html_template)
# js plot function logic:
html_template = insert_plot_data_logic(html_template)
file('charts.html', 'w').write(html_template.replace('__CHART_DATA_GOES_HERE__', sys.stdin.read()))
