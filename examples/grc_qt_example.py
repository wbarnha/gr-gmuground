#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Grc Qt Example
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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import gpredict
import guiextra
from gnuradio import qtgui

class grc_qt_example(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Grc Qt Example")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Grc Qt Example")
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

        self.settings = Qt.QSettings("GNU Radio", "grc_qt_example")

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
        self.snr = snr = 0
        self.sat = sat = 0
        self.state = state = int((sat == 0 and snr >= 0.387204) or (sat == 1 and snr >= 0.387204) or (sat == 2 and snr >= 0.280505) or (sat == 3 or sat == 4 or sat == 5 and snr >= 0.44457))
        self.samp_rate = samp_rate = 32000
        self.noise = noise = 0.01
        self.freq = freq = 1000
        self.amp = amp = 1

        ##################################################
        # Blocks
        ##################################################
        self._noise_range = Range(0, 1.0, 0.01, 0.01, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, 'Noise Amplitude', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_win)
        self._freq_range = Range(0, samp_rate/2.0, samp_rate/100.0, 1000, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, 'Signal Frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_win)
        self._amp_range = Range(0, 1.0, 0.01, 1, 200)
        self._amp_win = RangeWidget(self._amp_range, self.set_amp, 'Signal Amplitude', "counter_slider", float)
        self.top_grid_layout.addWidget(self._amp_win)
        # Create the options list
        self._sat_options = [0,1,2,3,4,5,6]
        # Create the labels list
        self._sat_labels = ["Generic 1k2 FSK","FloripaSat 1","ITASAT 1","AO-73","JY1SAT (JO-97)","NAYIF-1 (EO-88)"]
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
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'QT GUI Plot', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            False #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)
        self.guiextra_ledindicator_0 = self._guiextra_ledindicator_0_win = guiextra.GrLEDIndicator("State", "green", "red", state, 40, 1, 1, 1, self)
        self.guiextra_ledindicator_0 = self._guiextra_ledindicator_0_win
        self.top_grid_layout.addWidget(self._guiextra_ledindicator_0_win)
        self.gpredict_VarToMsg_0 = gpredict.VarToMsgPair('state')
        self.gpredict_MsgPairToVar_0 = gpredict.MsgPairToVar(self.set_snr)
        self.digital_probe_mpsk_snr_est_c_0 = digital.probe_mpsk_snr_est_c(3, 10000, 0.001)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 0.0j],
            noise_seed=-42,
            block_tags=False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq, amp, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_probe_mpsk_snr_est_c_0, 'snr'), (self.gpredict_MsgPairToVar_0, 'inpair'))
        self.msg_connect((self.gpredict_VarToMsg_0, 'msgout'), (self.guiextra_ledindicator_0, 'state'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_probe_mpsk_snr_est_c_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "grc_qt_example")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.set_state(int((self.sat == 0 and self.snr >= 0.387204) or (self.sat == 1 and self.snr >= 0.387204) or (self.sat == 2 and self.snr >= 0.280505) or (self.sat == 3 or self.sat == 4 or self.sat == 5 and self.snr >= 0.44457)))

    def get_sat(self):
        return self.sat

    def set_sat(self, sat):
        self.sat = sat
        self._sat_callback(self.sat)
        self.set_state(int((self.sat == 0 and self.snr >= 0.387204) or (self.sat == 1 and self.snr >= 0.387204) or (self.sat == 2 and self.snr >= 0.280505) or (self.sat == 3 or self.sat == 4 or self.sat == 5 and self.snr >= 0.44457)))

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        self.gpredict_VarToMsg_0.variableChanged(self.state)
        self.guiextra_ledindicator_0.setState(self.state)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.channels_channel_model_0.set_noise_voltage(self.noise)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.analog_sig_source_x_0.set_frequency(self.freq)

    def get_amp(self):
        return self.amp

    def set_amp(self, amp):
        self.amp = amp
        self.analog_sig_source_x_0.set_amplitude(self.amp)



def main(top_block_cls=grc_qt_example, options=None):

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
