#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
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

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from phase_sync import phase_sync  # grc-generated hier_block
from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")

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
        self.samp_rate = samp_rate = 2e6
        self.delay = delay = 0

        ##################################################
        # Blocks
        ##################################################
        self._delay_tool_bar = Qt.QToolBar(self)
        self._delay_tool_bar.addWidget(Qt.QLabel('delay' + ": "))
        self._delay_line_edit = Qt.QLineEdit(str(self.delay))
        self._delay_tool_bar.addWidget(self._delay_line_edit)
        self._delay_line_edit.returnPressed.connect(
            lambda: self.set_delay(int(str(self._delay_line_edit.text()))))
        self.top_grid_layout.addWidget(self._delay_tool_bar)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024*10, #size
            samp_rate, #samp_rate
            "", #name
            5 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.01)
        self.qtgui_time_sink_x_0.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Ch1', 'Ch2 (Delay)', 'Ch2 (Delay and Phase Adjust)', 'Ch2 (No Change)', 'Ch2 (Phase Adjust)',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(5):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.phase_sync_0_0 = phase_sync()
        self.phase_sync_0 = phase_sync()
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            10,
            firdes.low_pass(
                1,
                samp_rate,
                1e3,
                1e2,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            10,
            firdes.low_pass(
                1,
                samp_rate,
                1e3,
                1e2,
                firdes.WIN_HAMMING,
                6.76))
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/wbarnhart/presync/145mhzch2', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/wbarnhart/presync/145mhzch1', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, int(samp_rate*146e6*111e-6/(145e6)))
        self.blocks_complex_to_real_0_0_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_complex_to_real_0_0_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_complex_to_real_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 3))
        self.connect((self.blocks_complex_to_real_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 4))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.phase_sync_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.phase_sync_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.phase_sync_0_0, 1))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_complex_to_real_0_0_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.phase_sync_0_0, 0))
        self.connect((self.phase_sync_0, 0), (self.blocks_complex_to_real_0_0_0, 0))
        self.connect((self.phase_sync_0_0, 0), (self.blocks_complex_to_real_0_0_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_delay_0_0_0.set_dly(int(self.samp_rate*146e6*111e-6/(145e6)))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 1e3, 1e2, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 1e3, 1e2, firdes.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        Qt.QMetaObject.invokeMethod(self._delay_line_edit, "setText", Qt.Q_ARG("QString", str(self.delay)))



def main(top_block_cls=top_block, options=None):

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
