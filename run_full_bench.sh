#!/bin/bash
. ./set_env.sh
make clean
make -j$(nproc)
LLP=${LD_LIBRARY_PATH}
LPR=${LD_PRELOAD}
sudo -E nice -n-20 ionice -c1 -n0 sudo -u $USER LD_LIBRARY_PATH=${LLP} LD_PRELOAD=${LPR} python bench.py
./generate_html.sh
