#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GMU Ground
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

from Maximal_Combining import Maximal_Combining  # grc-generated hier_block
from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from Selective_Combining import Selective_Combining  # grc-generated hier_block
from Selective_Combining_BPSK import Selective_Combining_BPSK  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import fosphor
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from satnogs_cw_decoder import satnogs_cw_decoder  # grc-generated hier_block
import gpredict
import limesdr
import satellites.core
from gnuradio import qtgui

class sdrangel_source(gr.top_block, Qt.QWidget):

    def __init__(self, freq=145.85e6, gpredict_port=4532):
        gr.top_block.__init__(self, "GMU Ground")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GMU Ground")
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

        self.settings = Qt.QSettings("GNU Radio", "sdrangel_source")

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
        self.trans_width = trans_width = 100e3
        self.sat_type = sat_type = {0:'3CAT-2',1:'AO-73',2:'FloripaSat 1',3:'ITASAT 1',4:'JY1-Sat',5:'Nayif-1',6:'UKube-1'}
        self.sat = sat = 0
        self.samp_rate = samp_rate = 0.5e6
        self.gain = gain = 30
        self.cut_freq = cut_freq = 100e3
        self.com = com = 0
        self.channel = channel = 0

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
        self._gain_range = Range(0, 60, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win)
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
        self.top_grid_layout.addWidget(self._com_group_box)
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
        self.top_grid_layout.addWidget(self._channel_group_box)
        self._trans_width_range = Range(10e3, 500e3, 500, 100e3, 200)
        self._trans_width_win = RangeWidget(self._trans_width_range, self.set_trans_width, 'Transition width', "counter_slider", float)
        self.top_grid_layout.addWidget(self._trans_width_win)
        self.satnogs_cw_decoder_0 = satnogs_cw_decoder(
            antenna="",
            bfo_freq=1e3,
            bw=0.0,
            decoded_data_file_path="/tmp/.satnogs/data/data",
            dev_args="",
            doppler_correction_per_sec=20,
            enable_iq_dump=0,
            file_path="test.wav",
            gain=0.0,
            iq_file_path="/tmp/iq.dat",
            lo_offset=100e3,
            rigctl_port=4532,
            rx_freq=100e6,
            samp_rate_rx=0.0,
            soapy_rx_device="driver=invalid",
            udp_IP="127.0.0.1",
            udp_port=16887,
            waterfall_file_path="/tmp/waterfall.dat",
            wpm=20,
        )
        self.satellites_satellite_decoder_0 = satellites.core.gr_satellites_flowgraph(name = sat_type[sat], samp_rate = samp_rate, grc_block = True, iq = False)
        self.limesdr_source_0_1_0 = limesdr.source('', 0, '')


        self.limesdr_source_0_1_0.set_sample_rate(samp_rate)


        self.limesdr_source_0_1_0.set_center_freq(freq, 0)

        self.limesdr_source_0_1_0.set_bandwidth(1.5e6, 0)


        self.limesdr_source_0_1_0.set_digital_filter(samp_rate, 0)


        self.limesdr_source_0_1_0.set_gain(gain, 0)


        self.limesdr_source_0_1_0.set_antenna(2, 0)


        self.limesdr_source_0_1_0.calibrate(2.5e6, 0)
        self.gpredict_MsgPairToVar_0_0_0 = gpredict.MsgPairToVar(self.set_freq)
        self.fosphor_glfw_sink_c_0 = fosphor.glfw_sink_c()
        self.fosphor_glfw_sink_c_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_glfw_sink_c_0.set_frequency_range(freq, samp_rate)
        self._cut_freq_range = Range(1e3, samp_rate/2, 1e3, 100e3, 200)
        self._cut_freq_win = RangeWidget(self._cut_freq_range, self.set_cut_freq, 'Cutoff frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._cut_freq_win)
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_gr_complex*1, '127.0.0.1', 7356, 1472, True)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex*1, '127.0.0.1', 9090, 512-28, False)
        self.blocks_selector_1_0 = blocks.selector(gr.sizeof_gr_complex*1,channel,0)
        self.blocks_selector_1_0.set_enabled(True)
        self.blocks_selector_1 = blocks.selector(gr.sizeof_gr_complex*1,channel,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,com,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_message_debug_1 = blocks.message_debug()
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, int(samp_rate*146e6*269.1093e-6/freq))
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.Selective_Combining_BPSK_0 = Selective_Combining_BPSK(
            filter_alpha=1e-3,
            tag_samps=1000,
        )
        self.Selective_Combining_0 = Selective_Combining(
            filter_alpha=1e-3,
            tag_samps=1000,
        )
        self.Maximal_Combining_0 = Maximal_Combining(
            filter_alpha=1e-3,
            tag_samps=1000,
        )



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.fosphor_glfw_sink_c_0, 'freq'), (self.gpredict_MsgPairToVar_0_0_0, 'inpair'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.blocks_message_debug_1, 'print'))
        self.connect((self.Maximal_Combining_0, 0), (self.blocks_selector_0, 3))
        self.connect((self.Selective_Combining_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.Selective_Combining_BPSK_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.satellites_satellite_decoder_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.Maximal_Combining_0, 1))
        self.connect((self.blocks_delay_0_0_0, 0), (self.Selective_Combining_0, 1))
        self.connect((self.blocks_delay_0_0_0, 0), (self.Selective_Combining_BPSK_0, 1))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_selector_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.fosphor_glfw_sink_c_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.blocks_selector_1_0, 0), (self.Maximal_Combining_0, 0))
        self.connect((self.blocks_selector_1_0, 0), (self.Selective_Combining_0, 0))
        self.connect((self.blocks_selector_1_0, 0), (self.Selective_Combining_BPSK_0, 0))
        self.connect((self.blocks_selector_1_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_udp_source_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.blocks_udp_source_0, 0), (self.satnogs_cw_decoder_0, 0))
        self.connect((self.limesdr_source_0_1_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.limesdr_source_0_1_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.limesdr_source_0_1_0, 0), (self.blocks_selector_1_0, 0))
        self.connect((self.limesdr_source_0_1_0, 0), (self.blocks_selector_1_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "sdrangel_source")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.blocks_delay_0_0_0.set_dly(int(self.samp_rate*146e6*269.1093e-6/self.freq))
        self.fosphor_glfw_sink_c_0.set_frequency_range(self.freq, self.samp_rate)
        self.limesdr_source_0_1_0.set_center_freq(self.freq, 0)

    def get_gpredict_port(self):
        return self.gpredict_port

    def set_gpredict_port(self, gpredict_port):
        self.gpredict_port = gpredict_port

    def get_trans_width(self):
        return self.trans_width

    def set_trans_width(self, trans_width):
        self.trans_width = trans_width

    def get_sat_type(self):
        return self.sat_type

    def set_sat_type(self, sat_type):
        self.sat_type = sat_type

    def get_sat(self):
        return self.sat

    def set_sat(self, sat):
        self.sat = sat
        self._sat_callback(self.sat)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_delay_0_0_0.set_dly(int(self.samp_rate*146e6*269.1093e-6/self.freq))
        self.fosphor_glfw_sink_c_0.set_frequency_range(self.freq, self.samp_rate)
        self.limesdr_source_0_1_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_source_0_1_0.set_digital_filter(self.samp_rate, 1)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.limesdr_source_0_1_0.set_gain(self.gain, 0)
        self.limesdr_source_0_1_0.set_gain(self.gain, 1)

    def get_cut_freq(self):
        return self.cut_freq

    def set_cut_freq(self, cut_freq):
        self.cut_freq = cut_freq

    def get_com(self):
        return self.com

    def set_com(self, com):
        self.com = com
        self._com_callback(self.com)
        self.blocks_selector_0.set_input_index(self.com)

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self._channel_callback(self.channel)
        self.blocks_selector_1.set_input_index(self.channel)
        self.blocks_selector_1_0.set_input_index(self.channel)


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--freq", dest="freq", type=eng_float, default="145.85M",
        help="Set frequency [default=%(default)r]")
    parser.add_argument(
        "--gpredict-port", dest="gpredict_port", type=intx, default=4532,
        help="Set GPredict port [default=%(default)r]")
    return parser


def main(top_block_cls=sdrangel_source, options=None):
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
