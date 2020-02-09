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

class snr_selector(gr.sync_block):
    """
    docstring for block snr_selector
    """
    def __init__(self,item1_size,item2_size):
        gr.sync_block.__init__(self,
            name="snr_selector",
            in_sig=[item1_size,item1_size,item2_size,item2_size],
            out_sig=[item2_size])


    def work(self, input_items, output_items):
        if input_items[0][0] <= input_items[1][0]:
            output_items[0][:] = input_items[2]
        else:
            output_items[0][:] = input_items[3]
        return len(output_items[0])
