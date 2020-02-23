#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Main Block for GMU Ground
# Author: William Barnhart
# GNU Radio version: 3.8.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from Selective_Combining import Selective_Combining  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import gpredict
import limesdr
from gnuradio import qtgui

class main(gr.top_block, Qt.QWidget):

    def __init__(self, freq=145.85e6, gpredict_port=4532):
        gr.top_block.__init__(self, "Main Block for GMU Ground")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Main Block for GMU Ground")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "main")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.freq = freq
        self.gpredict_port = gpredict_port

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.4e6
        self.gain = gain = 30

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 60, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win)
        self.limesdr_source_0_1 = limesdr.source('0009070105C62E09', 2, '')


        self.limesdr_source_0_1.set_sample_rate(samp_rate)


        self.limesdr_source_0_1.set_center_freq(freq, 0)

        self.limesdr_source_0_1.set_bandwidth(1.5e6, 0)

        self.limesdr_source_0_1.set_bandwidth(1.5e6, 1)

        self.limesdr_source_0_1.set_digital_filter(samp_rate, 0)

        self.limesdr_source_0_1.set_digital_filter(samp_rate, 1)

        self.limesdr_source_0_1.set_gain(gain, 0)

        self.limesdr_source_0_1.set_gain(gain, 1)

        self.limesdr_source_0_1.set_antenna(2, 0)

        self.limesdr_source_0_1.set_antenna(2, 1)

        self.limesdr_source_0_1.calibrate(2.5e6, 0)

        self.limesdr_source_0_1.calibrate(2.5e6, 1)
        self.gpredict_doppler_0 = gpredict.doppler('localhost', gpredict_port, True)
        self.gpredict_MsgPairToVar_0 = gpredict.MsgPairToVar(self.set_freq)
        self.blocks_tcp_server_sink_0 = blocks.tcp_server_sink(gr.sizeof_gr_complex*1, '127.0.0.1', 9090, False)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, int(samp_rate*146e6*269.1093e-6/freq))
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, int(samp_rate*146e6*269.1093e-6/freq))
        self.Selective_Combining_0 = Selective_Combining(
            filter_alpha=1e-3,
            tag_samps=1000,
        )



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gpredict_doppler_0, 'state'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.gpredict_doppler_0, 'freq'), (self.gpredict_MsgPairToVar_0, 'inpair'))
        self.connect((self.Selective_Combining_0, 0), (self.blocks_tcp_server_sink_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.Selective_Combining_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.Selective_Combining_0, 1))
        self.connect((self.limesdr_source_0_1, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.limesdr_source_0_1, 1), (self.blocks_delay_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "main")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.blocks_delay_0_0.set_dly(int(self.samp_rate*146e6*269.1093e-6/self.freq))
        self.blocks_delay_0_0_0.set_dly(int(self.samp_rate*146e6*269.1093e-6/self.freq))
        self.limesdr_source_0_1.set_center_freq(self.freq, 0)

    def get_gpredict_port(self):
        return self.gpredict_port

    def set_gpredict_port(self, gpredict_port):
        self.gpredict_port = gpredict_port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_delay_0_0.set_dly(int(self.samp_rate*146e6*269.1093e-6/self.freq))
        self.blocks_delay_0_0_0.set_dly(int(self.samp_rate*146e6*269.1093e-6/self.freq))
        self.limesdr_source_0_1.set_digital_filter(self.samp_rate, 0)
        self.limesdr_source_0_1.set_digital_filter(self.samp_rate, 1)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.limesdr_source_0_1.set_gain(self.gain, 0)
        self.limesdr_source_0_1.set_gain(self.gain, 1)


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--freq", dest="freq", type=eng_float, default="145.85M",
        help="Set frequency [default=%(default)r]")
    parser.add_argument(
        "--gpredict-port", dest="gpredict_port", type=intx, default=4532,
        help="Set GPredict port [default=%(default)r]")
    return parser


def main(top_block_cls=main, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(freq=options.freq, gpredict_port=options.gpredict_port)
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
