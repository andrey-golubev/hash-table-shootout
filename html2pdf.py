#!/usr/bin/env python

# html2pdf.py requires pdfkit. Install:
# pip install pdfkit
#
# Extras for Debian/Ubuntu:
# apt install wkhtmltopdf

import pdfkit
pdfkit.from_file('charts.html', 'charts.pdf')
