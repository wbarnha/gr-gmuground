#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Main Block for GMU Ground
# Author: William Barnhart
# GNU Radio version: 3.8.1.0

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

from Combine_select import Combine_select  # grc-generated hier_block
from Delay_sync import Delay_sync  # grc-generated hier_block
from PyQt5 import Qt
import sip
from gnuradio import fosphor
from gnuradio.fft import window
from fmusbwide import fmusbwide  # grc-generated hier_block
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import gpredict
import satellites
import satellites.core
from gnuradio import qtgui

class main(gr.top_block, Qt.QWidget):

    def __init__(self, gpredict_port=4532, samp_rate=600e3):
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
        self.gpredict_port = gpredict_port
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.freq = freq = 146e6

        ##################################################
        # Blocks
        ##################################################
        self.satellites_satellite_decoder_0 = satellites.core.gr_satellites_flowgraph(file = '/usr/local/lib/python3/dist-packages/satellites/satyaml/ITASAT_1.yml', samp_rate = 48e3, grc_block = True, iq = False)
        self.satellites_print_timestamp_0 = satellites.print_timestamp('%Y-%m-%d %H:%M:%S', True)
        self.gpredict_MsgPairToVar_0_0_0 = gpredict.MsgPairToVar(self.set_freq)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(freq, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._fosphor_qt_sink_c_0_win)
        self.fmusbwide_0 = fmusbwide(
            decim=1,
            filter_width=20000,
            freq=146e6,
            offset=50e3,
            samp_rate=600e3,
        )

        self.top_grid_layout.addWidget(self.fmusbwide_0)
        self.blocks_message_debug_1 = blocks.message_debug()
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/wbarnhart/presync/145mhzch2', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/wbarnhart/presync/145mhzch1', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.Delay_sync_0 = Delay_sync(
            freq=146e6,
            samp_rate=600e3,
        )

        self.top_grid_layout.addWidget(self.Delay_sync_0)
        self.Combine_select_0 = Combine_select(
            filter_alpha=1e-3,
            samp_rate=600e3,
            tag_samps=1000,
        )

        self.top_grid_layout.addWidget(self.Combine_select_0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.fosphor_qt_sink_c_0, 'freq'), (self.gpredict_MsgPairToVar_0_0_0, 'inpair'))
        self.msg_connect((self.satellites_print_timestamp_0, 'out'), (self.blocks_message_debug_1, 'print_pdu'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.satellites_print_timestamp_0, 'in'))
        self.connect((self.Combine_select_0, 0), (self.fmusbwide_0, 0))
        self.connect((self.Combine_select_0, 0), (self.fosphor_qt_sink_c_0, 0))
        self.connect((self.Delay_sync_0, 1), (self.Combine_select_0, 1))
        self.connect((self.Delay_sync_0, 0), (self.Combine_select_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.Delay_sync_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.Delay_sync_0, 1))
        self.connect((self.fmusbwide_0, 0), (self.satellites_satellite_decoder_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "main")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_gpredict_port(self):
        return self.gpredict_port

    def set_gpredict_port(self, gpredict_port):
        self.gpredict_port = gpredict_port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.fosphor_qt_sink_c_0.set_frequency_range(self.freq, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.fosphor_qt_sink_c_0.set_frequency_range(self.freq, self.samp_rate)


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--gpredict-port", dest="gpredict_port", type=intx, default=4532,
        help="Set GPredict port [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default="600.0k",
        help="Set Sample Rate [default=%(default)r]")
    return parser


def main(top_block_cls=main, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(gpredict_port=options.gpredict_port, samp_rate=options.samp_rate)
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
