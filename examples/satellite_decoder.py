#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Satellite decoder example
# Author: Daniel Estevez
# Copyright: Daniel Estevez
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

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import satellites.core
from gnuradio import qtgui

class satellite_decoder(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Satellite decoder example")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Satellite decoder example")
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

        self.settings = Qt.QSettings("GNU Radio", "satellite_decoder")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.sat_type = sat_type = (41732,39444,44885,43786,43803,42017,40074)
        self.sat = sat = 0
        self.samp_rate = samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._sat_options = [0,1,2,3,4,5,6]
        # Create the labels list
        self._sat_labels = ["3CAT-2","AO-73","FloripaSat 1","ITASAT 1","JY1SAT (JO-97)","NAYIF-1 (EO-88)","UKUBE-1"]
        # Create the combo box
        self._sat_tool_bar = Qt.QToolBar(self)
        self._sat_tool_bar.addWidget(Qt.QLabel('Demo Satellite' + ": "))
        self._sat_combo_box = Qt.QComboBox()
        self._sat_tool_bar.addWidget(self._sat_combo_box)
        for _label in self._sat_labels: self._sat_combo_box.addItem(_label)
        self._sat_callback = lambda i: Qt.QMetaObject.invokeMethod(self._sat_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._sat_options.index(i)))
        self._sat_callback(self.sat)
        self._sat_combo_box.currentIndexChanged.connect(
            lambda i: self.set_sat(self._sat_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._sat_tool_bar)
        self.satellites_satellite_decoder_0_0_0_0_0_0_0_0 = satellites.core.gr_satellites_flowgraph(norad = sat_type[6], samp_rate = samp_rate, grc_block = True, iq = False)
        self.satellites_satellite_decoder_0_0_0_0_0_0_0 = satellites.core.gr_satellites_flowgraph(norad = sat_type[5], samp_rate = samp_rate, grc_block = True, iq = False)
        self.satellites_satellite_decoder_0_0_0_0_0_0 = satellites.core.gr_satellites_flowgraph(norad = sat_type[4], samp_rate = samp_rate, grc_block = True, iq = False)
        self.satellites_satellite_decoder_0_0_0_0_0 = satellites.core.gr_satellites_flowgraph(norad = sat_type[3], samp_rate = samp_rate, grc_block = True, iq = False)
        self.satellites_satellite_decoder_0_0_0_0 = satellites.core.gr_satellites_flowgraph(norad = sat_type[2], samp_rate = samp_rate, grc_block = True, iq = False)
        self.satellites_satellite_decoder_0_0_0 = satellites.core.gr_satellites_flowgraph(norad = sat_type[1], samp_rate = samp_rate, grc_block = True, iq = False)
        self.satellites_satellite_decoder_0_0 = satellites.core.gr_satellites_flowgraph(norad = sat_type[0], samp_rate = samp_rate, grc_block = True, iq = False)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            512, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Baseband', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/0.1)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/wbarnha/gr-satellites/satellite-recordings/itasat1.wav', True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,0,sat)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_message_debug_0_0 = blocks.message_debug()
        self.blocks_message_debug_0 = blocks.message_debug()



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_satellite_decoder_0_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_satellite_decoder_0_0_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_satellite_decoder_0_0_0_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_satellite_decoder_0_0_0_0_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_satellite_decoder_0_0_0_0_0_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_satellite_decoder_0_0_0_0_0_0_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_satellite_decoder_0_0_0_0_0_0_0_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.connect((self.blocks_selector_0, 0), (self.satellites_satellite_decoder_0_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.satellites_satellite_decoder_0_0_0, 0))
        self.connect((self.blocks_selector_0, 2), (self.satellites_satellite_decoder_0_0_0_0, 0))
        self.connect((self.blocks_selector_0, 3), (self.satellites_satellite_decoder_0_0_0_0_0, 0))
        self.connect((self.blocks_selector_0, 4), (self.satellites_satellite_decoder_0_0_0_0_0_0, 0))
        self.connect((self.blocks_selector_0, 5), (self.satellites_satellite_decoder_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_selector_0, 6), (self.satellites_satellite_decoder_0_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "satellite_decoder")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sat_type(self):
        return self.sat_type

    def set_sat_type(self, sat_type):
        self.sat_type = sat_type

    def get_sat(self):
        return self.sat

    def set_sat(self, sat):
        self.sat = sat
        self._sat_callback(self.sat)
        self.blocks_selector_0.set_output_index(self.sat)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)



def main(top_block_cls=satellite_decoder, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
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
