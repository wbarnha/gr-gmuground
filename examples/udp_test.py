#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: wbarnhart
# GNU Radio version: 3.8.0.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation

class udp_test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Blocks
        ##################################################
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/wbarnhart/satellite-recordings/itasat1.wav', True)
        self.blocks_udp_sink_0_0 = blocks.udp_sink(gr.sizeof_short*1, 'Localhost', 7355, 1472, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_short*1, 48000,True)
        self.blocks_float_to_short_0_0 = blocks.float_to_short(1, 32767)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_short_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_udp_sink_0_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_short_0_0, 0))



def main(top_block_cls=udp_test, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
