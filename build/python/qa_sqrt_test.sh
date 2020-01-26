#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/wbarnhart/gr-gmuground/python
export PATH=/home/wbarnhart/gr-gmuground/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/wbarnhart/gr-gmuground/build/swig:$PYTHONPATH
/usr/bin/python2 /home/wbarnhart/gr-gmuground/python/qa_sqrt.py 
