#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class snr_selector(gr.sync_block):
    """
    Takes two floating point values corresponding to SNR and two complex signals. SNR1 corresponds to Sig1 and SNR corresponds to Sig2. The output of the block is a complex signal, either Sig1 or Sig2, dependning on which signal has a larger SNR. If both signals are equal in SNR, the block will default to producing Sig1.
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="SNR Selector",
            in_sig=[numpy.float32, numpy.float32, numpy.complex64, numpy.complex64],
            out_sig=[numpy.complex64])


    def work(self, input_items, output_items):
        if input_items[0][0] <= input_items[1][0]:
                output_items[0][:] = input_items[2]
        else:
                output_items[0][:] = input_items[3]
        return len(output_items[0])

