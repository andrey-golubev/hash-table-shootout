#!/bin/bash
make clean
make -j$(nproc)
python bench.py
./generate_html.sh
