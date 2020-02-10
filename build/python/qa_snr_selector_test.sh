#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/newuser/gr-gmuground/python
export PATH=/home/newuser/gr-gmuground/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/newuser/gr-gmuground/build/swig:$PYTHONPATH
/usr/bin/python2 /home/newuser/gr-gmuground/python/qa_snr_selector.py 
