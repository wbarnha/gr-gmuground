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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
import display
from gnuradio import fosphor
from gnuradio.fft import window
from Selective_Combining import Selective_Combining  # grc-generated hier_block
from Selective_Combining_BPSK import Selective_Combining_BPSK  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import datetime
import filerepeater
import gpredict
import guiextra
import inspector
import limesdr
import satellites.core
import satnogs
from gnuradio import qtgui

class dual_lime(gr.top_block, Qt.QWidget):

    def __init__(self, gpredict_port=4532, offset=50e3, samp_rate=2.048e6, wpm=20):
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
        self.wpm = wpm

        ##################################################
        # Variables
        ##################################################
        self.freq = freq = 145.93*1e6
        self.doppler_freq = doppler_freq = freq
        self.audio_samp_rate = audio_samp_rate = 48000
        self.variable_cw_decoder_0 = variable_cw_decoder_0 = satnogs.cw_decoder_make(audio_samp_rate/4, 512, 512-8, wpm, 10, 0.90, 4, 8, 96)
        self.transition_bw = transition_bw = 10e3
        self.time_delay = time_delay = 158e-12*(freq-145e6)+111e-6
        self.sig_save = sig_save = 2
        self.save = save = 0
        self.sat_type = sat_type = {0:'3CAT-2',1:'AO-73',2:'FloripaSat 1',3:'ITASAT 1',4:'JY1-Sat',5:'Nayif-1',6:'UKube-1'}
        self.sat = sat = 0
        self.guiextra_msgdigitalnumbercontrol_0 = guiextra_msgdigitalnumbercontrol_0 = 145.8e6
        self.gain = gain = 30
        self.freqshift = freqshift = 146930e3-146411e3
        self.freq_shift = freq_shift = doppler_freq-freq
        self.decimation = decimation = 1
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
        self._gain_range = Range(0, 60, 1, 30, 70)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Gain [dB]', "counter_slider", int)
        self.top_grid_layout.addWidget(self._gain_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
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
        if int == bool:
        	self._save_choices = {'Pressed': bool(1), 'Released': bool(0)}
        elif int == str:
        	self._save_choices = {'Pressed': "1".replace("'",""), 'Released': "0".replace("'","")}
        else:
        	self._save_choices = {'Pressed': 1, 'Released': 0}

        _save_toggle_button = guiextra.ToggleButton(self.set_save, 'Save Data', self._save_choices, False,"'value'".replace("'",""))
        _save_toggle_button.setColors("default","default","default","default")
        self.save = _save_toggle_button

        self.top_grid_layout.addWidget(_save_toggle_button, 5, 1, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.satnogs_frame_decoder_0 = satnogs.frame_decoder(variable_cw_decoder_0, 8 * 1)
        self.satellites_satellite_decoder_0 = satellites.core.gr_satellites_flowgraph(file = '/usr/local/lib/python3/dist-packages/satellites/satyaml/ITASAT_1.yml', samp_rate = 48e3, grc_block = True, iq = False)
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
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(samp_rate/48e3)+1,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            512, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            audio_samp_rate, #bw
            'Baseband', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/0.1)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.Misc_layout_0.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            int(decimation),
            firdes.low_pass(
                1,
                samp_rate,
                3000,
                1e3,
                firdes.WIN_HAMMING,
                6.76))
        self.limesdr_source_0_0_0 = limesdr.source('', 0, '')


        self.limesdr_source_0_0_0.set_sample_rate(samp_rate)


        self.limesdr_source_0_0_0.set_center_freq(freq, 0)

        self.limesdr_source_0_0_0.set_bandwidth(1.5e6, 0)


        self.limesdr_source_0_0_0.set_digital_filter(samp_rate, 0)


        self.limesdr_source_0_0_0.set_gain(gain, 0)


        self.limesdr_source_0_0_0.set_antenna(255, 0)


        self.limesdr_source_0_0_0.calibrate(2.5e6, 0)
        self.inspector_signal_detector_cvf_0 = inspector.signal_detector_cvf(samp_rate, 4096, firdes.WIN_BLACKMAN_hARRIS, -90, 0.9, False, 0.2, 0.0001, 10, '')
        self.inspector_qtgui_sink_vf_0 = inspector.qtgui_inspector_sink_vf(
          samp_rate,
          4096,
          freq,
          1,
          1,
          False
        )
        self._inspector_qtgui_sink_vf_0_win = sip.wrapinstance(self.inspector_qtgui_sink_vf_0.pyqwidget(), Qt.QWidget)

        self.Display_layout_2.addWidget(self._inspector_qtgui_sink_vf_0_win)
        self._guiextra_msgdigitalnumbercontrol_0_msgdigctl_win = guiextra.MsgDigitalNumberControl(lbl = 'Frequency', minFreqHz = 80e6, maxFreqHz=400e6, parent=self,  ThousandsSeparator=",",backgroundColor="black",fontColor="white", varCallback=self.set_guiextra_msgdigitalnumbercontrol_0,outputmsgname="'freq'".replace("'",""))
        self._guiextra_msgdigitalnumbercontrol_0_msgdigctl_win.setValue(145.8e6)
        self._guiextra_msgdigitalnumbercontrol_0_msgdigctl_win.setReadOnly(False)
        self.guiextra_msgdigitalnumbercontrol_0 = self._guiextra_msgdigitalnumbercontrol_0_msgdigctl_win

        self.top_grid_layout.addWidget(self._guiextra_msgdigitalnumbercontrol_0_msgdigctl_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.gpredict_doppler_0 = gpredict.doppler('localhost', gpredict_port, True)
        self.gpredict_MsgPairToVar_0_0_0 = gpredict.MsgPairToVar(self.set_freq)
        self.gpredict_MsgPairToVar_0 = gpredict.MsgPairToVar(self.set_doppler_freq)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1, samp_rate, samp_rate/(2*decimation), transition_bw), samp_rate/2, samp_rate)
        self.fosphor_qt_sink_c_0_0_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_0_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(freq, samp_rate)
        self._fosphor_qt_sink_c_0_0_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_0_0.pyqwidget(), Qt.QWidget)
        self.Display_layout_0.addWidget(self._fosphor_qt_sink_c_0_0_0_win)
        self.filerepeater_StateToBool_0 = filerepeater.StateToBool()
        self.filerepeater_AdvFileSink_0 = filerepeater.AdvFileSink(1, gr.sizeof_gr_complex*1, '/home/stars/', 'gr_record', freq, samp_rate, 0, 0,False,False,False, 8,False,False)
        self.blocks_selector_2 = blocks.selector(gr.sizeof_gr_complex*1,sig_save,0)
        self.blocks_selector_2.set_enabled(False)
        self.blocks_selector_1_0 = blocks.selector(gr.sizeof_gr_complex*1,channel,0)
        self.blocks_selector_1_0.set_enabled(True)
        self.blocks_selector_1 = blocks.selector(gr.sizeof_gr_complex*1,channel,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,com,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_message_debug_0_0 = blocks.message_debug()
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_delay_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, abs(int(samp_rate*146e6*time_delay/freq))*int((samp_rate*146e6*time_delay/freq)<0))
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, int(samp_rate*146e6*time_delay/freq)*int((samp_rate*146e6*time_delay/freq)>0))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_shift, 1, 0, 0)
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
        self.msg_connect((self.fosphor_qt_sink_c_0_0_0, 'freq'), (self.gpredict_MsgPairToVar_0, 'inpair'))
        self.msg_connect((self.gpredict_doppler_0, 'state'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.gpredict_doppler_0, 'freq'), (self.gpredict_MsgPairToVar_0, 'inpair'))
        self.msg_connect((self.guiextra_msgdigitalnumbercontrol_0, 'valueout'), (self.gpredict_MsgPairToVar_0_0_0, 'inpair'))
        self.msg_connect((self.inspector_signal_detector_cvf_0, 'map_out'), (self.inspector_qtgui_sink_vf_0, 'map_in'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.show_text_0, 'disp_pdu'))
        self.msg_connect((self.satnogs_frame_decoder_0, 'out'), (self.blocks_message_debug_0_0, 'print'))
        self.msg_connect((self.satnogs_frame_decoder_0, 'out'), (self.show_text_0, 'disp_pdu'))
        self.msg_connect((self.save, 'state'), (self.filerepeater_AdvFileSink_0, 'recordstate'))
        self.msg_connect((self.save, 'state'), (self.filerepeater_StateToBool_0, 'state'))
        self.connect((self.Maximal_Combining_0, 0), (self.blocks_selector_0, 3))
        self.connect((self.Selective_Combining_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.Selective_Combining_BPSK_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_sink_x_0, 0))
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
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.AptUI_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_selector_0, 0), (self.blocks_selector_2, 2))
        self.connect((self.blocks_selector_0, 0), (self.fosphor_qt_sink_c_0_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.inspector_signal_detector_cvf_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.blocks_selector_1_0, 0), (self.blocks_delay_0_0_0_0, 0))
        self.connect((self.blocks_selector_2, 0), (self.filerepeater_AdvFileSink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.inspector_signal_detector_cvf_0, 0), (self.inspector_qtgui_sink_vf_0, 0))
        self.connect((self.limesdr_source_0_0_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.limesdr_source_0_0_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.limesdr_source_0_0_0, 0), (self.blocks_selector_1_0, 1))
        self.connect((self.limesdr_source_0_0_0, 0), (self.blocks_selector_1_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.satnogs_frame_decoder_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_complex_to_real_0, 0))

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

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_delay_0_0_0.set_dly(int(self.samp_rate*146e6*self.time_delay/self.freq)*int((self.samp_rate*146e6*self.time_delay/self.freq)>0))
        self.blocks_delay_0_0_0_0.set_dly(abs(int(self.samp_rate*146e6*self.time_delay/self.freq))*int((self.samp_rate*146e6*self.time_delay/self.freq)<0))
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/(2*self.decimation), self.transition_bw))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.samp_rate/2)
        self.inspector_qtgui_sink_vf_0.set_samp_rate(self.samp_rate)
        self.inspector_signal_detector_cvf_0.set_samp_rate(self.samp_rate)
        self.limesdr_source_0_0_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_source_0_0_0.set_digital_filter(self.samp_rate/10, 1)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 3000, 1e3, firdes.WIN_HAMMING, 6.76))

    def get_wpm(self):
        return self.wpm

    def set_wpm(self, wpm):
        self.wpm = wpm

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
        self.inspector_qtgui_sink_vf_0.set_cfreq(self.freq)
        self.limesdr_source_0_0_0.set_center_freq(self.freq, 0)
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.audio_samp_rate)

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.set_freq_shift(self.doppler_freq-self.freq)

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.audio_samp_rate)

    def get_variable_cw_decoder_0(self):
        return self.variable_cw_decoder_0

    def set_variable_cw_decoder_0(self, variable_cw_decoder_0):
        self.variable_cw_decoder_0 = variable_cw_decoder_0

    def get_transition_bw(self):
        return self.transition_bw

    def set_transition_bw(self, transition_bw):
        self.transition_bw = transition_bw
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/(2*self.decimation), self.transition_bw))

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

    def get_sat_type(self):
        return self.sat_type

    def set_sat_type(self, sat_type):
        self.sat_type = sat_type

    def get_sat(self):
        return self.sat

    def set_sat(self, sat):
        self.sat = sat
        self._sat_callback(self.sat)

    def get_guiextra_msgdigitalnumbercontrol_0(self):
        return self.guiextra_msgdigitalnumbercontrol_0

    def set_guiextra_msgdigitalnumbercontrol_0(self, guiextra_msgdigitalnumbercontrol_0):
        self.guiextra_msgdigitalnumbercontrol_0 = guiextra_msgdigitalnumbercontrol_0

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.limesdr_source_0_0_0.set_gain(self.gain, 0)
        self.limesdr_source_0_0_0.set_gain(self.gain, 1)

    def get_freqshift(self):
        return self.freqshift

    def set_freqshift(self, freqshift):
        self.freqshift = freqshift

    def get_freq_shift(self):
        return self.freq_shift

    def set_freq_shift(self, freq_shift):
        self.freq_shift = freq_shift
        self.analog_sig_source_x_0_0.set_frequency(self.freq_shift)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/(2*self.decimation), self.transition_bw))

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
        "--samp-rate", dest="samp_rate", type=eng_float, default="2.048M",
        help="Set Sample Rate [default=%(default)r]")
    parser.add_argument(
        "--wpm", dest="wpm", type=intx, default=20,
        help="Set wpm [default=%(default)r]")
    return parser


def main(top_block_cls=dual_lime, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(gpredict_port=options.gpredict_port, offset=options.offset, samp_rate=options.samp_rate, wpm=options.wpm)
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
