#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Satellite Test
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
import display
from gnuradio import fosphor
from gnuradio.fft import window
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import datetime
import limesdr
import satellites.core
import satellites.hier
from gnuradio import qtgui

class satellite_lab(gr.top_block, Qt.QWidget):

    def __init__(self, gpredict_port=4532, offset=50e3, samp_rate=2.4e6):
        gr.top_block.__init__(self, "Satellite Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Satellite Test")
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

        self.settings = Qt.QSettings("GNU Radio", "satellite_lab")

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
        self.offset = offset
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.freq = freq = 145.93*1e6
        self.doppler_freq = doppler_freq = freq
        self.txgain = txgain = 1
        self.transition_bw = transition_bw = 10e3
        self.time_delay = time_delay = 158e-12*(freq-145e6)+111e-6
        self.sat_type = sat_type = (41732,39444,44885,43786,43803,42017,40074)
        self.sat = sat = 0
        self.gain = gain = 30
        self.freq_shift = freq_shift = doppler_freq-freq
        self.decimation = decimation = 50
        self.com = com = 0
        self.channel = channel = 0
        self.audio_samp_rate = audio_samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self._txgain_range = Range(0, 60, 1, 1, 70)
        self._txgain_win = RangeWidget(self._txgain_range, self.set_txgain, 'TX Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._txgain_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = Range(0, 60, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'RX Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.Misc = Qt.QTabWidget()
        self.Misc_widget_0 = Qt.QWidget()
        self.Misc_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Misc_widget_0)
        self.Misc_grid_layout_0 = Qt.QGridLayout()
        self.Misc_layout_0.addLayout(self.Misc_grid_layout_0)
        self.Misc.addTab(self.Misc_widget_0, 'Translated Baseband')
        self.Misc_widget_1 = Qt.QWidget()
        self.Misc_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Misc_widget_1)
        self.Misc_grid_layout_1 = Qt.QGridLayout()
        self.Misc_layout_1.addLayout(self.Misc_grid_layout_1)
        self.Misc.addTab(self.Misc_widget_1, 'Telemetry')
        self.top_grid_layout.addWidget(self.Misc, 6, 0, 1, 2)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.Display = Qt.QTabWidget()
        self.Display_widget_0 = Qt.QWidget()
        self.Display_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Display_widget_0)
        self.Display_grid_layout_0 = Qt.QGridLayout()
        self.Display_layout_0.addLayout(self.Display_grid_layout_0)
        self.Display.addTab(self.Display_widget_0, 'Waterfall')
        self.Display_widget_1 = Qt.QWidget()
        self.Display_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Display_widget_1)
        self.Display_grid_layout_1 = Qt.QGridLayout()
        self.Display_layout_1.addLayout(self.Display_grid_layout_1)
        self.Display.addTab(self.Display_widget_1, 'NOAA')
        self.Display_widget_2 = Qt.QWidget()
        self.Display_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Display_widget_2)
        self.Display_grid_layout_2 = Qt.QGridLayout()
        self.Display_layout_2.addLayout(self.Display_grid_layout_2)
        self.Display.addTab(self.Display_widget_2, 'Detection')
        self.top_grid_layout.addWidget(self.Display, 0, 2, 7, 4)
        for r in range(0, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.show_text_0 = display.show_text()
        self._show_text_0_win = sip.wrapinstance(self.show_text_0.pyqwidget(), Qt.QWidget)
        self.Misc_layout_1.addWidget(self._show_text_0_win)
        self.satellites_satellite_decoder_0 = satellites.core.gr_satellites_flowgraph(file = '/usr/local/lib/python3/dist-packages/satellites/satyaml/ITASAT_1.yml', samp_rate = audio_samp_rate, grc_block = True, iq = False)
        self.satellites_rms_agc_0 = satellites.hier.rms_agc(alpha=1e-2, reference=1.0)
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
        self.top_grid_layout.addWidget(self._sat_tool_bar, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=48,
                decimation=200,
                taps=None,
                fractional_bw=None)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            512, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            audio_samp_rate, #bw
            'Baseband', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/0.1)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.Misc_layout_0.addWidget(self._qtgui_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
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
        self.Display_layout_1.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0_0_0 = filter.interp_fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                audio_samp_rate,
                3000,
                1e3,
                firdes.WIN_HAMMING,
                6.76))
        self.limesdr_source_0_0_0 = limesdr.source('', 0, '')


        self.limesdr_source_0_0_0.set_sample_rate(samp_rate)


        self.limesdr_source_0_0_0.set_center_freq(freq, 0)

        self.limesdr_source_0_0_0.set_bandwidth(1.5e6, 0)


        self.limesdr_source_0_0_0.set_digital_filter(samp_rate/10, 0)


        self.limesdr_source_0_0_0.set_gain(gain, 0)


        self.limesdr_source_0_0_0.set_antenna(255, 0)


        self.limesdr_source_0_0_0.calibrate(2.5e6, 0)
        self.limesdr_sink_0_0 = limesdr.sink('', 0, '', '')


        self.limesdr_sink_0_0.set_sample_rate(samp_rate)


        self.limesdr_sink_0_0.set_center_freq(145.93e6, 0)

        self.limesdr_sink_0_0.set_bandwidth(5e6, 0)


        self.limesdr_sink_0_0.set_digital_filter(samp_rate/4, 0)


        self.limesdr_sink_0_0.set_gain(txgain, 0)


        self.limesdr_sink_0_0.set_antenna(255, 0)


        self.limesdr_sink_0_0.calibrate(2.5e6, 0)
        self.fosphor_qt_sink_c_0_0_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_0_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(freq, samp_rate)
        self._fosphor_qt_sink_c_0_0_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_0_0.pyqwidget(), Qt.QWidget)
        self.Display_layout_0.addWidget(self._fosphor_qt_sink_c_0_0_0_win)
        # Create the options list
        self._com_options = (0, 1, 2, 3, )
        # Create the labels list
        self._com_labels = ('Selective', 'Selective (BPSK Only)', 'Equal', 'Maximal', )
        # Create the combo box
        # Create the radio buttons
        self._com_group_box = Qt.QGroupBox('Combining Technique' + ": ")
        self._com_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._com_button_group = variable_chooser_button_group()
        self._com_group_box.setLayout(self._com_box)
        for i, _label in enumerate(self._com_labels):
            radio_button = Qt.QRadioButton(_label)
            self._com_box.addWidget(radio_button)
            self._com_button_group.addButton(radio_button, i)
        self._com_callback = lambda i: Qt.QMetaObject.invokeMethod(self._com_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._com_options.index(i)))
        self._com_callback(self.com)
        self._com_button_group.buttonClicked[int].connect(
            lambda i: self.set_com(self._com_options[i]))
        self.top_grid_layout.addWidget(self._com_group_box, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._channel_options = (0, 1, )
        # Create the labels list
        self._channel_labels = ('Vertical', 'Horizontal', )
        # Create the combo box
        # Create the radio buttons
        self._channel_group_box = Qt.QGroupBox('Delayed Channel' + ": ")
        self._channel_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._channel_button_group = variable_chooser_button_group()
        self._channel_group_box.setLayout(self._channel_box)
        for i, _label in enumerate(self._channel_labels):
            radio_button = Qt.QRadioButton(_label)
            self._channel_box.addWidget(radio_button)
            self._channel_button_group.addButton(radio_button, i)
        self._channel_callback = lambda i: Qt.QMetaObject.invokeMethod(self._channel_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._channel_options.index(i)))
        self._channel_callback(self.channel)
        self._channel_button_group.buttonClicked[int].connect(
            lambda i: self.set_channel(self._channel_options[i]))
        self.top_grid_layout.addWidget(self._channel_group_box, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/wbarnha/gr-satellites/satellite-recordings/itasat1.wav', True)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.audio_sink_0 = audio.sink(48000, '', True)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.show_text_0, 'disp_pdu'))
        self.connect((self.blocks_complex_to_real_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.satellites_satellite_decoder_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.limesdr_sink_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.limesdr_source_0_0_0, 0), (self.satellites_rms_agc_0, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.satellites_rms_agc_0, 0), (self.fosphor_qt_sink_c_0_0_0, 0))
        self.connect((self.satellites_rms_agc_0, 0), (self.rational_resampler_xxx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "satellite_lab")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_gpredict_port(self):
        return self.gpredict_port

    def set_gpredict_port(self, gpredict_port):
        self.gpredict_port = gpredict_port

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.limesdr_sink_0_0.set_digital_filter(self.samp_rate/4, 0)
        self.limesdr_sink_0_0.set_digital_filter(self.samp_rate, 1)
        self.limesdr_source_0_0_0.set_digital_filter(self.samp_rate/10, 0)
        self.limesdr_source_0_0_0.set_digital_filter(self.samp_rate/10, 1)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_doppler_freq(self.freq)
        self.set_freq_shift(self.doppler_freq-self.freq)
        self.set_time_delay(158e-12*(self.freq-145e6)+111e-6)
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.limesdr_source_0_0_0.set_center_freq(self.freq, 0)

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.set_freq_shift(self.doppler_freq-self.freq)

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.limesdr_sink_0_0.set_gain(self.txgain, 0)

    def get_transition_bw(self):
        return self.transition_bw

    def set_transition_bw(self, transition_bw):
        self.transition_bw = transition_bw

    def get_time_delay(self):
        return self.time_delay

    def set_time_delay(self, time_delay):
        self.time_delay = time_delay

    def get_sat_type(self):
        return self.sat_type

    def set_sat_type(self, sat_type):
        self.sat_type = sat_type

    def get_sat(self):
        return self.sat

    def set_sat(self, sat):
        self.sat = sat
        self._sat_callback(self.sat)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.limesdr_source_0_0_0.set_gain(self.gain, 0)
        self.limesdr_source_0_0_0.set_gain(self.gain, 1)

    def get_freq_shift(self):
        return self.freq_shift

    def set_freq_shift(self, freq_shift):
        self.freq_shift = freq_shift

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation

    def get_com(self):
        return self.com

    def set_com(self, com):
        self.com = com
        self._com_callback(self.com)

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self._channel_callback(self.channel)

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, 3000, 1e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.audio_samp_rate)


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--gpredict-port", dest="gpredict_port", type=intx, default=4532,
        help="Set GPredict port [default=%(default)r]")
    parser.add_argument(
        "--offset", dest="offset", type=eng_float, default="50.0k",
        help="Set Frequency Offset [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default="2.4M",
        help="Set Sample Rate [default=%(default)r]")
    return parser


def main(top_block_cls=satellite_lab, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(gpredict_port=options.gpredict_port, offset=options.offset, samp_rate=options.samp_rate)
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
