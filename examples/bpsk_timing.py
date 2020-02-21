#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Bpsk Timing
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

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio import fec
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
import limesdr
from gnuradio import qtgui

class bpsk_timing(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Bpsk Timing")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Bpsk Timing")
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

        self.settings = Qt.QSettings("GNU Radio", "bpsk_timing")

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
        self.time_bw = time_bw = 0
        self.spb = spb = 4.2563
        self.sig_amp = sig_amp = 1
        self.samp_rate = samp_rate = 2e6
        self.rolloff = rolloff = .35
        self.noise_amp = noise_amp = 0
        self.nfilts = nfilts = 32
        self.interpratio = interpratio = 1
        self.gain = gain = 30
        self.freq_offset = freq_offset = 0
        self.delay = delay = 0
        self.constellation = constellation = digital.constellation_bpsk().base()
        self.const = const = digital.bpsk_constellation()
        self.baseband = baseband = 915

        ##################################################
        # Blocks
        ##################################################
        self._time_bw_range = Range(0, .1, .001, 0, 200)
        self._time_bw_win = RangeWidget(self._time_bw_range, self.set_time_bw, 'Timing Loop BW', "counter_slider", float)
        self.top_grid_layout.addWidget(self._time_bw_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = Range(0, 60, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win)
        self._delay_tool_bar = Qt.QToolBar(self)
        self._delay_tool_bar.addWidget(Qt.QLabel('delay' + ": "))
        self._delay_line_edit = Qt.QLineEdit(str(self.delay))
        self._delay_tool_bar.addWidget(self._delay_line_edit)
        self._delay_line_edit.returnPressed.connect(
            lambda: self.set_delay(int(str(self._delay_line_edit.text()))))
        self.top_grid_layout.addWidget(self._delay_tool_bar)
        self._baseband_tool_bar = Qt.QToolBar(self)
        self._baseband_tool_bar.addWidget(Qt.QLabel('RX Baseband [MHz]' + ": "))
        self._baseband_line_edit = Qt.QLineEdit(str(self.baseband))
        self._baseband_tool_bar.addWidget(self._baseband_line_edit)
        self._baseband_line_edit.returnPressed.connect(
            lambda: self.set_baseband(eng_notation.str_to_num(str(self._baseband_line_edit.text()))))
        self.top_grid_layout.addWidget(self._baseband_tool_bar)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=25,
                decimation=6,
                taps=None,
                fractional_bw=None)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 3)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(True)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(True)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
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


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            'Scope Plot', #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
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


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 30, 0, 15, 2)
        for r in range(30, 45):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_0_1_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            3
        )
        self.qtgui_number_sink_0_0_1_0.set_update_time(0.1)
        self.qtgui_number_sink_0_0_1_0.set_title("Synchronized")

        labels = ['BER', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', 'Consolidated', '', '',
            '', '', '', '', '']
        colors = [("blue", "red"), ("blue", "red"), ("blue", "red"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(3):
            self.qtgui_number_sink_0_0_1_0.set_min(i, 0)
            self.qtgui_number_sink_0_0_1_0.set_max(i, 1)
            self.qtgui_number_sink_0_0_1_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_1_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_1_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_1_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_1_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_1_0.enable_autoscale(True)
        self._qtgui_number_sink_0_0_1_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_1_0_win)
        self._noise_amp_range = Range(0, 1, .001, 0, 200)
        self._noise_amp_win = RangeWidget(self._noise_amp_range, self.set_noise_amp, 'Channel Noise', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_amp_win, 3, 2, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.limesdr_source_0 = limesdr.source('0009070105C62E09', 2, '')


        self.limesdr_source_0.set_sample_rate(2e6)


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
        self._interpratio_range = Range(.99, 1.01, 0.0001, 1, 200)
        self._interpratio_win = RangeWidget(self._interpratio_range, self.set_interpratio, 'Timing Offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._interpratio_win, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_offset_range = Range(-.5, .5, .01, 0, 200)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, 'Frequency Offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_offset_win, 4, 2, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fec_ber_bf_0_1_0 = fec.ber_bf(False, 100, -7.0)
        self.fec_ber_bf_0_1 = fec.ber_bf(False, 100, -7.0)
        self.fec_ber_bf_0 = fec.ber_bf(False, 100, -7.0)
        self.digital_symbol_sync_xx_0_0 = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            8,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            8,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(time_bw, 4, False)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(time_bw, 4, False)
        self.digital_constellation_modulator_1 = digital.generic_mod(
            constellation=constellation,
            differential=False,
            samples_per_symbol=int(2*25/6),
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.digital_constellation_decoder_cb_0_0_0_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_constellation_decoder_cb_0_0_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_cma_equalizer_cc_0_0 = digital.cma_equalizer_cc(15, 1, 1, 4)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(15, 1, 1, 4)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_delay_1 = blocks.delay(gr.sizeof_gr_complex*1, 0)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 10000))), True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_1, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.fec_ber_bf_0_1, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.qtgui_time_sink_x_2, 1))
        self.connect((self.blocks_delay_1, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_delay_1, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.digital_symbol_sync_xx_0_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0, 0), (self.fec_ber_bf_0_1_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0_0, 0), (self.fec_ber_bf_0_1, 1))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0_0, 0), (self.fec_ber_bf_0_1_0, 1))
        self.connect((self.digital_constellation_modulator_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_constellation_decoder_cb_0_0_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.fec_ber_bf_0, 0), (self.qtgui_number_sink_0_0_1_0, 0))
        self.connect((self.fec_ber_bf_0_1, 0), (self.qtgui_number_sink_0_0_1_0, 1))
        self.connect((self.fec_ber_bf_0_1_0, 0), (self.qtgui_number_sink_0_0_1_0, 2))
        self.connect((self.limesdr_source_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.limesdr_source_0, 1), (self.digital_cma_equalizer_cc_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.limesdr_sink_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "bpsk_timing")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_time_bw(self):
        return self.time_bw

    def set_time_bw(self, time_bw):
        self.time_bw = time_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.time_bw)
        self.digital_costas_loop_cc_0_0.set_loop_bandwidth(self.time_bw)

    def get_spb(self):
        return self.spb

    def set_spb(self, spb):
        self.spb = spb

    def get_sig_amp(self):
        return self.sig_amp

    def set_sig_amp(self, sig_amp):
        self.sig_amp = sig_amp

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.limesdr_sink_0_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_sink_0_0.set_digital_filter(self.samp_rate, 1)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts

    def get_interpratio(self):
        return self.interpratio

    def set_interpratio(self, interpratio):
        self.interpratio = interpratio

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.limesdr_sink_0_0.set_gain(self.gain, 0)
        self.limesdr_source_0.set_gain(self.gain, 0)
        self.limesdr_source_0.set_gain(self.gain, 1)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        Qt.QMetaObject.invokeMethod(self._delay_line_edit, "setText", Qt.Q_ARG("QString", str(self.delay)))

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_baseband(self):
        return self.baseband

    def set_baseband(self, baseband):
        self.baseband = baseband
        Qt.QMetaObject.invokeMethod(self._baseband_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.baseband)))
        self.limesdr_sink_0_0.set_center_freq(self.baseband*1e6, 0)
        self.limesdr_source_0.set_center_freq(self.baseband*1e6, 0)



def main(top_block_cls=bpsk_timing, options=None):

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
