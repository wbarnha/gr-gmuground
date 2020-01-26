#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 William Barnhart.
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

class sqrt(gr.sync_block):
    """
    Takes a complex float as an input and produces the square root of the input using Numpy.
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Square Root",
            in_sig=[numpy.complex64],
            out_sig=[numpy.complex64])

    def forecast(self, ninput_items_required, noutput_items):
        #setup size of input_items[i] for work call
        size = len(ninput_items_required)
        for i in range(size):
            ninput_items_required[i] = noutput_items

    def work(self, input_items, output_items):
        output_items[0][:] = numpy.sqrt(input_items[0])
        #consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])
