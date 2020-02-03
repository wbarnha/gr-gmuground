/* -*- c++ -*- */

#define GMUGROUND_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "gmuground_swig_doc.i"

%{
#include "gmuground/channel_calibrate.h"
%}

%include "gmuground/channel_calibrate.h"
GR_SWIG_BLOCK_MAGIC2(gmuground, channel_calibrate);


