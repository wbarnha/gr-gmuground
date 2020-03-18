#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: File Decoder
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

from PyQt5 import Qt
from gnuradio import qtgui
import display
import sip
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from rms_agc import rms_agc  # grc-generated hier_block
import satellites
from gnuradio import qtgui

class file_decoder(gr.top_block, Qt.QWidget):

    def __init__(self, bfo=1.5e3):
        gr.top_block.__init__(self, "File Decoder")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("File Decoder")
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

        self.settings = Qt.QSettings("GNU Radio", "file_decoder")

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
        self.bfo = bfo

        ##################################################
        # Variables
        ##################################################
        self.samp_per_sym = samp_per_sym = 8
        self.nfilts = nfilts = 16
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist([-1, 1], [0, 1],
        2, 1).base()
        self.samp_rate = samp_rate = 48000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(samp_per_sym), 0.35, 11*samp_per_sym*nfilts)

        ##################################################
        # Blocks
        ##################################################
        self.show_text_1 = display.show_text()
        self._show_text_1_win = sip.wrapinstance(self.show_text_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._show_text_1_win)
        self.satellites_nrzi_decode_0 = satellites.nrzi_decode()
        self.satellites_hdlc_deframer_0 = satellites.hdlc_deframer(check_fcs=False, max_length=10000)
        self.rms_agc_0 = rms_agc(
            alpha=1e-2,
            reference=0.5,
        )
        self.freq_xlating_fir_filter_xxx_0_0_1 = filter.freq_xlating_fir_filter_fcf(5, firdes.low_pass(1, samp_rate, 1300, 500), bfo, samp_rate)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samp_per_sym, 0.1, rrc_taps, nfilts, nfilts/2, 0.05, 2)
        self.digital_lms_dd_equalizer_cc_0_0 = digital.lms_dd_equalizer_cc(2, 0.03, 2, variable_constellation_0)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(samp_per_sym, 0.350, 100, 0.010)
        self.digital_costas_loop_cc_0_0_0_0 = digital.costas_loop_cc(0.04, 2, False)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/wbarnha/iqtest', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self.show_text_1, 'disp_pdu'))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.freq_xlating_fir_filter_xxx_0_0_1, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_complex_to_real_1, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.satellites_nrzi_decode_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0_0, 0), (self.digital_lms_dd_equalizer_cc_0_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_lms_dd_equalizer_cc_0_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0_0_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_1, 0), (self.rms_agc_0, 0))
        self.connect((self.rms_agc_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.satellites_nrzi_decode_0, 0), (self.satellites_hdlc_deframer_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "file_decoder")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_bfo(self):
        return self.bfo

    def set_bfo(self, bfo):
        self.bfo = bfo
        self.freq_xlating_fir_filter_xxx_0_0_1.set_center_freq(self.bfo)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samp_per_sym), 0.35, 11*self.samp_per_sym*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samp_per_sym), 0.35, 11*self.samp_per_sym*self.nfilts))

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0_0_1.set_taps(firdes.low_pass(1, self.samp_rate, 1300, 500))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--bfo", dest="bfo", type=eng_float, default="1.5k",
        help="Set carrier frequency of the BPSK signal [default=%(default)r]")
    return parser


def main(top_block_cls=file_decoder, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(bfo=options.bfo)
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
