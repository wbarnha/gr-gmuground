#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM Receiver
# Author: Lime Microsystems
<<<<<<< HEAD
# GNU Radio version: 3.8.1.0
=======
# GNU Radio version: 3.8.0.0
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1

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
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
<<<<<<< HEAD
import pmt
=======
<<<<<<< HEAD
import pmt
=======
import numpy
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257
from gnuradio import digital
from gnuradio import fec
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
<<<<<<< HEAD
=======
from phase_sync import phase_sync  # grc-generated hier_block
<<<<<<< HEAD
=======
import limesdr
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257
from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM Receiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM Receiver")
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
<<<<<<< HEAD
        self.trans_width = trans_width = 10e3
        self.sps = sps = 7
=======
<<<<<<< HEAD
        self.volume = volume = 1
=======
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
        self.trans_width = trans_width = 100e3
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257
        self.samp_rate = samp_rate = 2e6
        self.offset = offset = int(1e8)
        self.gain = gain = 30
        self.delay = delay = 20
        self.cut_freq = cut_freq = 25e3
        self.constellation = constellation = digital.constellation_bpsk().base()
        self.baseband = baseband = 915

        ##################################################
        # Blocks
        ##################################################
        self._trans_width_range = Range(10e3, 500e3, 500, 10e3, 200)
        self._trans_width_win = RangeWidget(self._trans_width_range, self.set_trans_width, 'Transition width', "counter_slider", float)
        self.top_grid_layout.addWidget(self._trans_width_win)
<<<<<<< HEAD
        self._delay_tool_bar = Qt.QToolBar(self)
        self._delay_tool_bar.addWidget(Qt.QLabel('delay' + ": "))
        self._delay_line_edit = Qt.QLineEdit(str(self.delay))
        self._delay_tool_bar.addWidget(self._delay_line_edit)
        self._delay_line_edit.returnPressed.connect(
            lambda: self.set_delay(int(str(self._delay_line_edit.text()))))
        self.top_grid_layout.addWidget(self._delay_tool_bar)
        self._cut_freq_range = Range(1e3, samp_rate/2, 1e3, 25e3, 200)
=======
<<<<<<< HEAD
        self._cut_freq_range = Range(1e3, samp_rate/2, 1e3, 500e3, 200)
        self._cut_freq_win = RangeWidget(self._cut_freq_range, self.set_cut_freq, 'Cutoff frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._cut_freq_win)
        self._volume_range = Range(0, 10, 0.1, 1, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, 'Volume', "counter_slider", float)
        self.top_grid_layout.addWidget(self._volume_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            4 #number of inputs
=======
        self._gain_range = Range(0, 70, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win)
        self._cut_freq_range = Range(1e3, samp_rate/2, 1e3, 500e3, 200)
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257
        self._cut_freq_win = RangeWidget(self._cut_freq_range, self.set_cut_freq, 'Cutoff frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._cut_freq_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            1*samp_rate, #samp_rate
            "", #name
<<<<<<< HEAD
            2 #number of inputs
=======
            3 #number of inputs
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257
        )
        self.qtgui_time_sink_x_0.set_update_time(0.01)
        self.qtgui_time_sink_x_0.set_y_axis(-0.01, 0.01)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


<<<<<<< HEAD
        labels = ['Ch1', 'Ch2', 'Phase Correction', '', 'Vertical',
=======
        labels = ['Horizontal', 'Peaks', 'Phase Difference', '', 'Vertical',
<<<<<<< HEAD
            '', 'Transmitted Re', 'Tx Im', '', '']
=======
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257
            '', '', '', '', '']
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'black', 'green', 'black', 'dark red',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
<<<<<<< HEAD
        styles = [3, 1, 1, 1, 1,
=======
        styles = [1, 1, 1, 1, 1,
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


<<<<<<< HEAD
        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
=======
<<<<<<< HEAD
        for i in range(4):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
=======
        for i in range(6):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 30, 0, 15, 2)
        for r in range(30, 45):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0_0.set_update_time(0.1)
        self.qtgui_number_sink_0_0.set_title('')

        labels = ['Horizontal BER', 'Vertical BER', 'Sync BER', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("blue", "red"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0.set_min(i, 0)
            self.qtgui_number_sink_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(True)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.pyqwidget(), Qt.QWidget)
<<<<<<< HEAD
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_win)
=======
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.1)
        self.qtgui_number_sink_0.set_title("Horizontal")

        labels = ['BER', '', '', '', '',
            '', '', '', '', '']
        units = ['x10^-6', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1e6, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, 0)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(True)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
<<<<<<< HEAD
=======
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            baseband*1e6, #fc
            samp_rate, #bw
            "Transmiting data", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win)
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
        self.phase_sync_0 = phase_sync()
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                cut_freq,
                trans_width,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                cut_freq,
                trans_width,
                firdes.WIN_HAMMING,
                6.76))
<<<<<<< HEAD
        self._gain_range = Range(0, 60, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win)
        self.fec_ber_bf_0_0_1_0 = fec.ber_bf(False, 100, -7.0)
        self.digital_constellation_decoder_cb_0_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(constellation)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/wbarnhart/ch2', False, offset, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/wbarnhart/ch1', False, offset, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self._baseband_tool_bar = Qt.QToolBar(self)
        self._baseband_tool_bar.addWidget(Qt.QLabel('RX Baseband [MHz]' + ": "))
        self._baseband_line_edit = Qt.QLineEdit(str(self.baseband))
        self._baseband_tool_bar.addWidget(self._baseband_line_edit)
        self._baseband_line_edit.returnPressed.connect(
            lambda: self.set_baseband(eng_notation.str_to_num(str(self._baseband_line_edit.text()))))
        self.top_grid_layout.addWidget(self._baseband_tool_bar)
=======
        # Create the options list
        self._lna_path_options = (255, 1, 2, 3, )
        # Create the labels list
        self._lna_path_labels = ('Auto', 'H', 'L', 'W', )
        # Create the combo box
        self._lna_path_tool_bar = Qt.QToolBar(self)
        self._lna_path_tool_bar.addWidget(Qt.QLabel('LNA Path' + ": "))
        self._lna_path_combo_box = Qt.QComboBox()
        self._lna_path_tool_bar.addWidget(self._lna_path_combo_box)
        for _label in self._lna_path_labels: self._lna_path_combo_box.addItem(_label)
        self._lna_path_callback = lambda i: Qt.QMetaObject.invokeMethod(self._lna_path_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._lna_path_options.index(i)))
        self._lna_path_callback(self.lna_path)
        self._lna_path_combo_box.currentIndexChanged.connect(
            lambda i: self.set_lna_path(self._lna_path_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._lna_path_tool_bar)
<<<<<<< HEAD
        self._gain_range = Range(0, 70, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win)
        self.fec_ber_bf_0_0_1_0 = fec.ber_bf(False, 10000, -7.0)
        self.fec_ber_bf_0_0 = fec.ber_bf(False, 10000, -7.0)
        self.fec_ber_bf_0 = fec.ber_bf(False, 10000, -7.0)
        self.digital_constellation_decoder_cb_0_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(constellation)
        self.blocks_multiply_const_vxx_0_1_1 = blocks.multiply_const_cc(0.02)
        self.blocks_multiply_const_vxx_0_1_0 = blocks.multiply_const_cc(100)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_cc(100)
        self.blocks_file_source_1 = blocks.file_source(gr.sizeof_char*1, '/home/stars/bittest', False, 0, 0)
        self.blocks_file_source_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/stars/bpsktest', False, 0, 0)
        self.blocks_file_source_0_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/stars/ch2', False, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/stars/ch1', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_real_0_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self._baseband_tool_bar = Qt.QToolBar(self)
        self._baseband_tool_bar.addWidget(Qt.QLabel('RX Baseband [MHz]' + ": "))
        self._baseband_line_edit = Qt.QLineEdit(str(self.baseband))
        self._baseband_tool_bar.addWidget(self._baseband_line_edit)
        self._baseband_line_edit.returnPressed.connect(
            lambda: self.set_baseband(eng_notation.str_to_num(str(self._baseband_line_edit.text()))))
        self.top_grid_layout.addWidget(self._baseband_tool_bar)
=======
        self.limesdr_source_0 = limesdr.source('0009070105C62E09', 2, '')


        self.limesdr_source_0.set_sample_rate(samp_rate)

        self.limesdr_source_0.set_oversampling(32)

        self.limesdr_source_0.set_center_freq(baseband*1e6, 0)

        self.limesdr_source_0.set_bandwidth(2e6, 0)

        self.limesdr_source_0.set_bandwidth(2e6, 1)

        self.limesdr_source_0.set_digital_filter(1.8e6, 0)

        self.limesdr_source_0.set_digital_filter(1.8e6, 1)

        self.limesdr_source_0.set_gain(gain, 0)

        self.limesdr_source_0.set_gain(gain, 1)

        self.limesdr_source_0.set_antenna(3, 0)

        self.limesdr_source_0.set_antenna(3, 1)

        self.limesdr_source_0.calibrate(2.5e6, 0)

        self.limesdr_source_0.calibrate(2.5e6, 1)
        self.limesdr_sink_0_0 = limesdr.sink('1D423F7CD55972', 0, '', '')


        self.limesdr_sink_0_0.set_sample_rate(samp_rate)


        self.limesdr_sink_0_0.set_center_freq(baseband*1e6, 0)

        self.limesdr_sink_0_0.set_bandwidth(5e6, 0)


        self.limesdr_sink_0_0.set_digital_filter(samp_rate, 0)


        self.limesdr_sink_0_0.set_gain(gain, 0)


        self.limesdr_sink_0_0.set_antenna(255, 0)


        self.limesdr_sink_0_0.calibrate(2.5e6, 0)
        self.fec_ber_bf_0_0_1_0 = fec.ber_bf(False, 10000, -7.0)
        self.fec_ber_bf_0_0 = fec.ber_bf(False, 10000, -7.0)
        self.fec_ber_bf_0 = fec.ber_bf(False, 10000, -7.0)
        self.digital_constellation_modulator_1 = digital.generic_mod(
            constellation=constellation,
            differential=True,
            samples_per_symbol=2,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.digital_constellation_decoder_cb_0_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(constellation)
        self.blocks_multiply_const_vxx_0_1_0 = blocks.multiply_const_cc(1)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_cc(1)
        self.analog_random_source_x = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 10000))), True)
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257



        ##################################################
        # Connections
        ##################################################
<<<<<<< HEAD
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_delay_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.fec_ber_bf_0_0_1_0, 0))
=======
<<<<<<< HEAD
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_complex_to_real_0_0_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_complex_to_real_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 3))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_multiply_const_vxx_0_1_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_file_source_0_0_0, 0), (self.blocks_multiply_const_vxx_0_1_1, 0))
        self.connect((self.blocks_file_source_1, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.blocks_file_source_1, 0), (self.fec_ber_bf_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1_1, 0), (self.blocks_complex_to_real_0_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.fec_ber_bf_0_0_1_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.fec_ber_bf_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0, 0), (self.fec_ber_bf_0_0_1_0, 1))
        self.connect((self.fec_ber_bf_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.fec_ber_bf_0_0, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.fec_ber_bf_0_0_1_0, 0), (self.qtgui_number_sink_0_0_1_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.phase_sync_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.phase_sync_0, 1))
        self.connect((self.phase_sync_0, 0), (self.blocks_complex_to_real_0_0_0, 0))
        self.connect((self.phase_sync_0, 0), (self.digital_constellation_decoder_cb_0_0_0, 0))
=======
        self.connect((self.analog_random_source_x, 0), (self.digital_constellation_modulator_1, 0))
        self.connect((self.analog_random_source_x, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.analog_random_source_x, 0), (self.fec_ber_bf_0_0, 0))
        self.connect((self.analog_random_source_x, 0), (self.fec_ber_bf_0_0_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.fec_ber_bf_0_0, 1))
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257
        self.connect((self.digital_constellation_decoder_cb_0_0_0, 0), (self.fec_ber_bf_0_0_1_0, 1))
        self.connect((self.fec_ber_bf_0_0_1_0, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_constellation_decoder_cb_0_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
<<<<<<< HEAD
=======
        self.connect((self.low_pass_filter_0_0, 0), (self.phase_sync_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.phase_sync_0, 0), (self.digital_constellation_decoder_cb_0_0_0, 0))
        self.connect((self.phase_sync_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.rational_resampler_xxx_0, 0), (self.limesdr_sink_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

<<<<<<< HEAD
    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume

=======
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
    def get_trans_width(self):
        return self.trans_width

    def set_trans_width(self, trans_width):
        self.trans_width = trans_width
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
<<<<<<< HEAD
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(1*self.samp_rate)
=======
<<<<<<< HEAD
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
=======
        self.limesdr_sink_0_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_sink_0_0.set_digital_filter(self.samp_rate, 1)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.baseband*1e6, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(2*self.samp_rate)
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
<<<<<<< HEAD

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        Qt.QMetaObject.invokeMethod(self._delay_line_edit, "setText", Qt.Q_ARG("QString", str(self.delay)))
        self.blocks_delay_0.set_dly(self.delay)
        self.blocks_delay_0_0.set_dly(self.delay)
=======
<<<<<<< HEAD
=======
        self.limesdr_sink_0_0.set_gain(self.gain, 0)
        self.limesdr_source_0.set_gain(self.gain, 0)
        self.limesdr_source_0.set_gain(self.gain, 1)
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257

    def get_cut_freq(self):
        return self.cut_freq

    def set_cut_freq(self, cut_freq):
        self.cut_freq = cut_freq
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_baseband(self):
        return self.baseband

    def set_baseband(self, baseband):
        self.baseband = baseband
        Qt.QMetaObject.invokeMethod(self._baseband_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.baseband)))
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
        self.limesdr_sink_0_0.set_center_freq(self.baseband*1e6, 0)
        self.limesdr_source_0.set_center_freq(self.baseband*1e6, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.baseband*1e6, self.samp_rate)
>>>>>>> 63d271765910b7316f7339ab0780300d6b54e1d1
>>>>>>> 5544c1f8cc364a34470453dee70f14c209457257



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