/* -*- c++ -*- */

#define GMUGROUND_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "gmuground_swig_doc.i"

%{
#include "gmuground/udp_text_display.h"
%}

%include "gmuground/udp_text_display.h"
GR_SWIG_BLOCK_MAGIC2(gmuground, udp_text_display);
