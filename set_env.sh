#!/bin/bash
export LD_LIBRARY_PATH=${HOME}/work/build/qt5/qtbase/lib/:${HOME}/work/build/5.15/qtbase/lib/:${LD_LIBRARY_PATH}
export LD_PRELOAD=~/work/build/5.15/qtbase/lib/libQt5Core.so
