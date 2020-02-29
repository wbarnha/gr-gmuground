/* -*- c++ -*- */

#define GMUGROUND_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "gmuground_swig_doc.i"

%{
#include "gmuground/interp_delay.h"
%}

%include "gmuground/interp_delay.h"
GR_SWIG_BLOCK_MAGIC2(gmuground, interp_delay);
