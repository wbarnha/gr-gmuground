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

from fmusbwide import fmusbwide  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import fosphor
from gnuradio.fft import window
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

    def __init__(self, bb_gain=20, filter_width=20000, freq=145.86e6, freq_corr=0, gpredict_port=4532, if_gain=20, offset=50e3, rf_gain=40):
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
        self.bb_gain = bb_gain
        self.filter_width = filter_width
        self.freq = freq
        self.freq_corr = freq_corr
        self.gpredict_port = gpredict_port
        self.if_gain = if_gain
        self.offset = offset
        self.rf_gain = rf_gain

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.gain = gain = 30
        self.doppler_freq = doppler_freq = freq

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 70, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.limesdr_source_0 = limesdr.source('', 0, '')


        self.limesdr_source_0.set_sample_rate(samp_rate)


        self.limesdr_source_0.set_center_freq(freq, 0)

        self.limesdr_source_0.set_bandwidth(1.5e6, 0)


        self.limesdr_source_0.set_digital_filter(samp_rate, 0)


        self.limesdr_source_0.set_gain(gain, 0)


        self.limesdr_source_0.set_antenna(255, 0)


        self.limesdr_source_0.calibrate(2.5e6, 0)
        self.gpredict_doppler_0 = gpredict.doppler('localhost', gpredict_port, True)
        self.gpredict_MsgPairToVar_0 = gpredict.MsgPairToVar(self.set_freq)
        self.fosphor_glfw_sink_c_0 = fosphor.glfw_sink_c()
        self.fosphor_glfw_sink_c_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_glfw_sink_c_0.set_frequency_range(freq, samp_rate)
        self.fmusbwide_0 = fmusbwide(
            filter_width=20000,
            freq=freq,
            offset=50e3,
        )

        self.top_grid_layout.addWidget(self.fmusbwide_0)
        self.blocks_throttle_0_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_message_debug_0 = blocks.message_debug()



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gpredict_doppler_0, 'state'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.gpredict_doppler_0, 'freq'), (self.gpredict_MsgPairToVar_0, 'inpair'))
        self.connect((self.blocks_throttle_0_0_0, 0), (self.fmusbwide_0, 0))
        self.connect((self.blocks_throttle_0_0_0, 0), (self.fosphor_glfw_sink_c_0, 0))
        self.connect((self.limesdr_source_0, 0), (self.blocks_throttle_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "main")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain

    def get_filter_width(self):
        return self.filter_width

    def set_filter_width(self, filter_width):
        self.filter_width = filter_width

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_doppler_freq(self.freq)
        self.fmusbwide_0.set_freq(self.freq)
        self.fosphor_glfw_sink_c_0.set_frequency_range(self.freq, self.samp_rate)
        self.limesdr_source_0.set_center_freq(self.freq, 0)

    def get_freq_corr(self):
        return self.freq_corr

    def set_freq_corr(self, freq_corr):
        self.freq_corr = freq_corr

    def get_gpredict_port(self):
        return self.gpredict_port

    def set_gpredict_port(self, gpredict_port):
        self.gpredict_port = gpredict_port

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0_0_0.set_sample_rate(self.samp_rate)
        self.fosphor_glfw_sink_c_0.set_frequency_range(self.freq, self.samp_rate)
        self.limesdr_source_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_source_0.set_digital_filter(self.samp_rate, 1)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.limesdr_source_0.set_gain(self.gain, 0)
        self.limesdr_source_0.set_gain(self.gain, 1)

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--bb-gain", dest="bb_gain", type=eng_float, default="20.0",
        help="Set baseband gain [default=%(default)r]")
    parser.add_argument(
        "--filter-width", dest="filter_width", type=eng_float, default="20.0k",
        help="Set FM filter width [default=%(default)r]")
    parser.add_argument(
        "-f", "--freq", dest="freq", type=eng_float, default="145.86M",
        help="Set frequency [default=%(default)r]")
    parser.add_argument(
        "--freq-corr", dest="freq_corr", type=eng_float, default="0.0",
        help="Set frequency correction (ppm) [default=%(default)r]")
    parser.add_argument(
        "--gpredict-port", dest="gpredict_port", type=intx, default=4532,
        help="Set GPredict port [default=%(default)r]")
    parser.add_argument(
        "--if-gain", dest="if_gain", type=eng_float, default="20.0",
        help="Set IF gain [default=%(default)r]")
    parser.add_argument(
        "--offset", dest="offset", type=eng_float, default="50.0k",
        help="Set centre frequency offset [default=%(default)r]")
    parser.add_argument(
        "--rf-gain", dest="rf_gain", type=eng_float, default="40.0",
        help="Set RF gain [default=%(default)r]")
    return parser


def main(top_block_cls=main, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(bb_gain=options.bb_gain, filter_width=options.filter_width, freq=options.freq, freq_corr=options.freq_corr, gpredict_port=options.gpredict_port, if_gain=options.if_gain, offset=options.offset, rf_gain=options.rf_gain)
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
