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
from gnuradio import blocks

class sample_count(gr.sync_block):
    """
    initial state: samples = 0
    samples +=1 when 1 sample is received
        if ctrl = 0:
        out = 0
        out = samples
    else:
        out = samples
        samples = 0
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="sample_count",
            in_sig=[item_size],
            out_sig=[item_size],
            samples=0)


    def work(self, input_items, output_items):
        self.samples += 1
        if input_items[1][0] > 0: 
            output_items[0][0] = samples
            samples = 0
        else:
            output_items[0][0] = 0
        return len(output_items[0])
