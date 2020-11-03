#!/bin/bash
python make_chart_data.py < output | python make_html.py
mkdir -p .html_report/
zip html_report.zip charts.html excanvas.min.js jquery.flot.js jquery.js
echo "You can open charts.html to see the results. Or use html_report.zip."
