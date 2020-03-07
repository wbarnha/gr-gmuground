#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Dual Lime RX
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

from AptUI import AptUI  # grc-generated hier_block
from Maximal_Combining import Maximal_Combining  # grc-generated hier_block
from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
import sip
from gnuradio import fosphor
from gnuradio.fft import window
from Selective_Combining import Selective_Combining  # grc-generated hier_block
from Selective_Combining_BPSK import Selective_Combining_BPSK  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
import datetime
import filerepeater
import gpredict
import satellites
import satellites.core
from gnuradio import qtgui

class dual_lime(gr.top_block, Qt.QWidget):

    def __init__(self, gpredict_port=4532, offset=50e3, samp_rate=600e3):
        gr.top_block.__init__(self, "Dual Lime RX")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Dual Lime RX")
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

        self.settings = Qt.QSettings("GNU Radio", "dual_lime")

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
        self.carrier = carrier = 145
        self.freq = freq = carrier*1e6
        self.doppler_freq = doppler_freq = freq
        self.time_delay = time_delay = 158e-12*(freq-145e6)+111e-6
        self.sig_save = sig_save = 2
        self.save = save = 0
        self.sat_type = sat_type = {0:'3CAT-2',1:'AO-73',2:'FloripaSat 1',3:'ITASAT 1',4:'JY1-Sat',5:'Nayif-1',6:'UKube-1'}
        self.sat = sat = 0
        self.gain = gain = 30
        self.freq_shift = freq_shift = doppler_freq-freq
        self.com = com = 0
        self.channel = channel = 0

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._sig_save_options = (2, 0, 1, )
        # Create the labels list
        self._sig_save_labels = ('Combined Signal', 'Ch. 1', 'Ch. 2', )
        # Create the combo box
        self._sig_save_tool_bar = Qt.QToolBar(self)
        self._sig_save_tool_bar.addWidget(Qt.QLabel('Channel to Save' + ": "))
        self._sig_save_combo_box = Qt.QComboBox()
        self._sig_save_tool_bar.addWidget(self._sig_save_combo_box)
        for _label in self._sig_save_labels: self._sig_save_combo_box.addItem(_label)
        self._sig_save_callback = lambda i: Qt.QMetaObject.invokeMethod(self._sig_save_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._sig_save_options.index(i)))
        self._sig_save_callback(self.sig_save)
        self._sig_save_combo_box.currentIndexChanged.connect(
            lambda i: self.set_sig_save(self._sig_save_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._sig_save_tool_bar, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.Display.addTab(self.Display_widget_2, 'Telemetry')
        self.top_grid_layout.addWidget(self.Display, 0, 2, 7, 4)
        for r in range(0, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        _save_check_box = Qt.QCheckBox('Save Data')
        self._save_choices = {True: 1, False: 0}
        self._save_choices_inv = dict((v,k) for k,v in self._save_choices.items())
        self._save_callback = lambda i: Qt.QMetaObject.invokeMethod(_save_check_box, "setChecked", Qt.Q_ARG("bool", self._save_choices_inv[i]))
        self._save_callback(self.save)
        _save_check_box.stateChanged.connect(lambda i: self.set_save(self._save_choices[bool(i)]))
        self.top_grid_layout.addWidget(_save_check_box, 5, 1, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.satellites_satellite_decoder_0 = satellites.core.gr_satellites_flowgraph(file = '/usr/local/lib/python3/dist-packages/satellites/satyaml/ITASAT_1.yml', samp_rate = 48e3, grc_block = True, iq = False)
        self.satellites_print_timestamp_0 = satellites.print_timestamp('%Y-%m-%d %H:%M:%S', True)
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
        self.gpredict_VarToMsg_0 = gpredict.VarToMsgPair('')
        self.gpredict_MsgPairToVar_0_0_0 = gpredict.MsgPairToVar(self.set_freq)
        self._gain_range = Range(0, 60, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1, samp_rate, 1500, 500), freq-doppler_freq+offset, samp_rate)
        self.fosphor_qt_sink_c_0_0_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_0_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(freq, samp_rate)
        self._fosphor_qt_sink_c_0_0_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_0_0.pyqwidget(), Qt.QWidget)
        self.Display_layout_0.addWidget(self._fosphor_qt_sink_c_0_0_0_win)
        self.filerepeater_StateToBool_0 = filerepeater.StateToBool()
        self.filerepeater_AdvFileSink_0 = filerepeater.AdvFileSink(1, gr.sizeof_gr_complex*1, '/home/presync/', 'gr_record', freq, samp_rate, 0, 0,False,False,False, 8,False,False)
        self._carrier_tool_bar = Qt.QToolBar(self)
        self._carrier_tool_bar.addWidget(Qt.QLabel('RX Freq [MHz]' + ": "))
        self._carrier_line_edit = Qt.QLineEdit(str(self.carrier))
        self._carrier_tool_bar.addWidget(self._carrier_line_edit)
        self._carrier_line_edit.returnPressed.connect(
            lambda: self.set_carrier(eng_notation.str_to_num(str(self._carrier_line_edit.text()))))
        self.top_grid_layout.addWidget(self._carrier_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_selector_2 = blocks.selector(gr.sizeof_gr_complex*1,sig_save,0)
        self.blocks_selector_2.set_enabled(True)
        self.blocks_selector_1_0 = blocks.selector(gr.sizeof_gr_complex*1,channel,0)
        self.blocks_selector_1_0.set_enabled(True)
        self.blocks_selector_1 = blocks.selector(gr.sizeof_gr_complex*1,channel,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,com,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_message_debug_1 = blocks.message_debug()
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/wbarnhart/presync/145mhzch2', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/wbarnhart/presync/145mhzch1', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, abs(int(samp_rate*146e6*time_delay/freq))*int((samp_rate*146e6*time_delay/freq)<0))
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, int(samp_rate*146e6*time_delay/freq)*int((samp_rate*146e6*time_delay/freq)>0))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1500, 1, 0, 0)
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
        self.AptUI_0 = AptUI()

        self.Display_layout_1.addWidget(self.AptUI_0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.filerepeater_StateToBool_0, 'bool'), (self.blocks_selector_2, 'en'))
        self.msg_connect((self.fosphor_qt_sink_c_0_0_0, 'freq'), (self.gpredict_MsgPairToVar_0_0_0, 'inpair'))
        self.msg_connect((self.gpredict_VarToMsg_0, 'msgout'), (self.filerepeater_AdvFileSink_0, 'recordstate'))
        self.msg_connect((self.gpredict_VarToMsg_0, 'msgout'), (self.filerepeater_StateToBool_0, 'state'))
        self.msg_connect((self.satellites_print_timestamp_0, 'out'), (self.blocks_message_debug_1, 'print_pdu'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.satellites_print_timestamp_0, 'in'))
        self.connect((self.Maximal_Combining_0, 0), (self.blocks_selector_0, 3))
        self.connect((self.Selective_Combining_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.Selective_Combining_BPSK_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.blocks_complex_to_real_0, 0), (self.satellites_satellite_decoder_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.Maximal_Combining_0, 1))
        self.connect((self.blocks_delay_0_0_0, 0), (self.Selective_Combining_0, 1))
        self.connect((self.blocks_delay_0_0_0, 0), (self.Selective_Combining_BPSK_0, 1))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_selector_2, 1))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.Maximal_Combining_0, 0))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.Selective_Combining_0, 0))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.Selective_Combining_BPSK_0, 0))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.blocks_selector_2, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_selector_1_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_selector_1_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.AptUI_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_selector_2, 2))
        self.connect((self.blocks_selector_0, 0), (self.fosphor_qt_sink_c_0_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.blocks_selector_1_0, 0), (self.blocks_delay_0_0_0_0, 0))
        self.connect((self.blocks_selector_2, 0), (self.filerepeater_AdvFileSink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "dual_lime")
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
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freq-self.doppler_freq+self.offset)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_delay_0_0_0.set_dly(int(self.samp_rate*146e6*self.time_delay/self.freq)*int((self.samp_rate*146e6*self.time_delay/self.freq)>0))
        self.blocks_delay_0_0_0_0.set_dly(abs(int(self.samp_rate*146e6*self.time_delay/self.freq))*int((self.samp_rate*146e6*self.time_delay/self.freq)<0))
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.samp_rate, 1500, 500))

    def get_carrier(self):
        return self.carrier

    def set_carrier(self, carrier):
        self.carrier = carrier
        Qt.QMetaObject.invokeMethod(self._carrier_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.carrier)))
        self.set_freq(self.carrier*1e6)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_doppler_freq(self.freq)
        self.set_freq_shift(self.doppler_freq-self.freq)
        self.set_time_delay(158e-12*(self.freq-145e6)+111e-6)
        self.blocks_delay_0_0_0.set_dly(int(self.samp_rate*146e6*self.time_delay/self.freq)*int((self.samp_rate*146e6*self.time_delay/self.freq)>0))
        self.blocks_delay_0_0_0_0.set_dly(abs(int(self.samp_rate*146e6*self.time_delay/self.freq))*int((self.samp_rate*146e6*self.time_delay/self.freq)<0))
        self.filerepeater_AdvFileSink_0.setCenterFrequency(self.freq)
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freq-self.doppler_freq+self.offset)

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.set_freq_shift(self.doppler_freq-self.freq)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freq-self.doppler_freq+self.offset)

    def get_time_delay(self):
        return self.time_delay

    def set_time_delay(self, time_delay):
        self.time_delay = time_delay
        self.blocks_delay_0_0_0.set_dly(int(self.samp_rate*146e6*self.time_delay/self.freq)*int((self.samp_rate*146e6*self.time_delay/self.freq)>0))
        self.blocks_delay_0_0_0_0.set_dly(abs(int(self.samp_rate*146e6*self.time_delay/self.freq))*int((self.samp_rate*146e6*self.time_delay/self.freq)<0))

    def get_sig_save(self):
        return self.sig_save

    def set_sig_save(self, sig_save):
        self.sig_save = sig_save
        self._sig_save_callback(self.sig_save)
        self.blocks_selector_2.set_input_index(self.sig_save)

    def get_save(self):
        return self.save

    def set_save(self, save):
        self.save = save
        self._save_callback(self.save)
        self.gpredict_VarToMsg_0.variableChanged(self.save)

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

    def get_freq_shift(self):
        return self.freq_shift

    def set_freq_shift(self, freq_shift):
        self.freq_shift = freq_shift

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
        "--gpredict-port", dest="gpredict_port", type=intx, default=4532,
        help="Set GPredict port [default=%(default)r]")
    parser.add_argument(
        "--offset", dest="offset", type=eng_float, default="50.0k",
        help="Set Frequency Offset [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default="600.0k",
        help="Set Sample Rate [default=%(default)r]")
    return parser


def main(top_block_cls=dual_lime, options=None):
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
