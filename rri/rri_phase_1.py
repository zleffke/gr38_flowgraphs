#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RRI Phase Comparison
# Author: zleffke
# GNU Radio version: 3.8.5.0-rc1

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
from datetime import datetime as dt; import string; import math; import numpy as np
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import gr_sigmf

from gnuradio import qtgui

class rri_phase_1(gr.top_block, Qt.QWidget):

    def __init__(self, avg_len=1024, decim=16, lpf_bw=1.5e3, nfft=2048):
        gr.top_block.__init__(self, "RRI Phase Comparison")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RRI Phase Comparison")
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

        self.settings = Qt.QSettings("GNU Radio", "rri_phase_1")

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
        self.avg_len = avg_len
        self.decim = decim
        self.lpf_bw = lpf_bw
        self.nfft = nfft

        ##################################################
        # Variables
        ##################################################
        self.rri_samp_rate = rri_samp_rate = 62500.33933
        self.fr_ratio = fr_ratio = rri_samp_rate / 32e3
        self.throttle = throttle = 10
        self.samp_rate = samp_rate = rri_samp_rate / fr_ratio
        self.k = k = -10*math.log10(nfft)
        self.fc = fc = 1.0e+07

        ##################################################
        # Blocks
        ##################################################
        self._throttle_tool_bar = Qt.QToolBar(self)
        self._throttle_tool_bar.addWidget(Qt.QLabel('throttle' + ": "))
        self._throttle_line_edit = Qt.QLineEdit(str(self.throttle))
        self._throttle_tool_bar.addWidget(self._throttle_line_edit)
        self._throttle_line_edit.returnPressed.connect(
            lambda: self.set_throttle(eng_notation.str_to_num(str(self._throttle_line_edit.text()))))
        self.top_layout.addWidget(self._throttle_tool_bar)
        self.main_tab = Qt.QTabWidget()
        self.main_tab_widget_0 = Qt.QWidget()
        self.main_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_0)
        self.main_tab_grid_layout_0 = Qt.QGridLayout()
        self.main_tab_layout_0.addLayout(self.main_tab_grid_layout_0)
        self.main_tab.addTab(self.main_tab_widget_0, 'Pre-d')
        self.main_tab_widget_1 = Qt.QWidget()
        self.main_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_1)
        self.main_tab_grid_layout_1 = Qt.QGridLayout()
        self.main_tab_layout_1.addLayout(self.main_tab_grid_layout_1)
        self.main_tab.addTab(self.main_tab_widget_1, 'Power')
        self.main_tab_widget_2 = Qt.QWidget()
        self.main_tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_2)
        self.main_tab_grid_layout_2 = Qt.QGridLayout()
        self.main_tab_layout_2.addLayout(self.main_tab_grid_layout_2)
        self.main_tab.addTab(self.main_tab_widget_2, 'Noise')
        self.main_tab_widget_3 = Qt.QWidget()
        self.main_tab_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_3)
        self.main_tab_grid_layout_3 = Qt.QGridLayout()
        self.main_tab_layout_3.addLayout(self.main_tab_grid_layout_3)
        self.main_tab.addTab(self.main_tab_widget_3, 'SNR')
        self.top_grid_layout.addWidget(self.main_tab, 0, 0, 4, 4)
        for r in range(0, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.sigmf_source_1 = gr_sigmf.source('/home/zleffke/captures/rri/wwv/20171023_083229/RRI_CHAN-B_20171023_083229_083326.sigmf-data', "cf32" + ("_le" if sys.byteorder == "little" else "_be"), False)
        self.sigmf_source_0 = gr_sigmf.source('/home/zleffke/captures/rri/wwv/20171023_083229/RRI_CHAN-A_20171023_083229_083326.sigmf-data', "cf32" + ("_le" if sys.byteorder == "little" else "_be"), False)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            64*8*2, #size
            samp_rate / decim, #samp_rate
            "", #name
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
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['SNR1', 'SNR2', 'NOISE1', 'NOISE2', 'Signal 5',
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
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_win, 6, 0, 1, 3)
        for r in range(6, 7):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 3):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            64, #size
            samp_rate / decim, #samp_rate
            "", #name
            4 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['PWR1', 'PWR2', 'NOISE1', 'NOISE2', 'Signal 5',
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


        for i in range(4):
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
        self.main_tab_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_win, 4, 0, 2, 3)
        for r in range(4, 6):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 3):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_VERT,
            2
        )
        self.qtgui_number_sink_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0.set_title("")

        labels = ['SNR1', 'SNR2', 'N1', 'N2', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(2):
            self.qtgui_number_sink_0_0.set_min(i, 0)
            self.qtgui_number_sink_0_0.set_max(i, 60)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_number_sink_0_0_win, 6, 3, 1, 1)
        for r in range(6, 7):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            4
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['P1', 'P2', 'N1', 'N2', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(4):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_number_sink_0_win, 4, 3, 2, 1)
        for r in range(4, 6):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            nfft, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            2
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(True)
        self.qtgui_freq_sink_x_1.set_fft_average(0.2)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_freq_sink_x_1_win, 0, 0, 4, 4)
        for r in range(0, 4):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.mmse_resampler_xx_0_0 = filter.mmse_resampler_cc(0, fr_ratio)
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, fr_ratio)
        self.low_pass_filter_0_0_0_0 = filter.fir_filter_ccf(
            decim,
            firdes.low_pass(
                1,
                samp_rate,
                lpf_bw,
                1e3,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0_0 = filter.fir_filter_ccf(
            decim,
            firdes.low_pass(
                1,
                samp_rate,
                lpf_bw,
                1e3,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            decim,
            firdes.low_pass(
                1,
                samp_rate,
                lpf_bw,
                1e3,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            decim,
            firdes.low_pass(
                1,
                samp_rate,
                lpf_bw,
                1e3,
                firdes.WIN_HAMMING,
                6.76))
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, rri_samp_rate*throttle,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, rri_samp_rate*throttle,True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, '', '')
        self.blocks_tag_debug_0.set_display(True)
        self.blocks_sub_xx_0_0 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_nlog10_ff_0_1 = blocks.nlog10_ff(10, 1, k)
        self.blocks_nlog10_ff_0_0_0 = blocks.nlog10_ff(10, 1, k)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, k+10*math.log10(decim)*0)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, k+10*math.log10(decim)*0)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_moving_average_xx_0_1 = blocks.moving_average_ff(int(avg_len), 1.0/(avg_len), 4000, 1)
        self.blocks_moving_average_xx_0_0_0 = blocks.moving_average_ff(int(avg_len), 1.0/(avg_len), 4000, 1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(int(avg_len), 1.0/(avg_len), 4000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int(avg_len), 1.0/(avg_len), 4000, 1)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_complex_to_mag_squared_0_1 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 8e3, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.sigmf_source_0, 'meta'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.sigmf_source_1, 'meta'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0_0, 0), (self.blocks_moving_average_xx_0_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_1, 0), (self.blocks_moving_average_xx_0_1, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0_0, 0), (self.blocks_nlog10_ff_0_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0_1, 0), (self.blocks_nlog10_ff_0_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.low_pass_filter_0_0_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.qtgui_number_sink_0, 1))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_nlog10_ff_0_0_0, 0), (self.blocks_sub_xx_0_0, 1))
        self.connect((self.blocks_nlog10_ff_0_0_0, 0), (self.qtgui_number_sink_0, 3))
        self.connect((self.blocks_nlog10_ff_0_0_0, 0), (self.qtgui_time_sink_x_0, 3))
        self.connect((self.blocks_nlog10_ff_0_1, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_nlog10_ff_0_1, 0), (self.qtgui_number_sink_0, 2))
        self.connect((self.blocks_nlog10_ff_0_1, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_sub_xx_0, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.qtgui_number_sink_0_0, 1))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.mmse_resampler_xx_0_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.blocks_complex_to_mag_squared_0_1, 0))
        self.connect((self.low_pass_filter_0_0_0_0, 0), (self.blocks_complex_to_mag_squared_0_0_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.qtgui_freq_sink_x_1, 1))
        self.connect((self.mmse_resampler_xx_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.mmse_resampler_xx_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.mmse_resampler_xx_0_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.sigmf_source_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.sigmf_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.sigmf_source_1, 0), (self.blocks_tag_debug_0, 1))
        self.connect((self.sigmf_source_1, 0), (self.blocks_throttle_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rri_phase_1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_avg_len(self):
        return self.avg_len

    def set_avg_len(self, avg_len):
        self.avg_len = avg_len
        self.blocks_moving_average_xx_0.set_length_and_scale(int(self.avg_len), 1.0/(self.avg_len))
        self.blocks_moving_average_xx_0_0.set_length_and_scale(int(self.avg_len), 1.0/(self.avg_len))
        self.blocks_moving_average_xx_0_0_0.set_length_and_scale(int(self.avg_len), 1.0/(self.avg_len))
        self.blocks_moving_average_xx_0_1.set_length_and_scale(int(self.avg_len), 1.0/(self.avg_len))

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate / self.decim)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate / self.decim)

    def get_lpf_bw(self):
        return self.lpf_bw

    def set_lpf_bw(self, lpf_bw):
        self.lpf_bw = lpf_bw
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.lpf_bw, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.lpf_bw, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.lpf_bw, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.lpf_bw, 1e3, firdes.WIN_HAMMING, 6.76))

    def get_nfft(self):
        return self.nfft

    def set_nfft(self, nfft):
        self.nfft = nfft
        self.set_k(-10*math.log10(self.nfft))

    def get_rri_samp_rate(self):
        return self.rri_samp_rate

    def set_rri_samp_rate(self, rri_samp_rate):
        self.rri_samp_rate = rri_samp_rate
        self.set_fr_ratio(self.rri_samp_rate / 32e3)
        self.set_samp_rate(self.rri_samp_rate / self.fr_ratio)
        self.blocks_throttle_0.set_sample_rate(self.rri_samp_rate*self.throttle)
        self.blocks_throttle_0_0.set_sample_rate(self.rri_samp_rate*self.throttle)

    def get_fr_ratio(self):
        return self.fr_ratio

    def set_fr_ratio(self, fr_ratio):
        self.fr_ratio = fr_ratio
        self.set_samp_rate(self.rri_samp_rate / self.fr_ratio)
        self.mmse_resampler_xx_0.set_resamp_ratio(self.fr_ratio)
        self.mmse_resampler_xx_0_0.set_resamp_ratio(self.fr_ratio)

    def get_throttle(self):
        return self.throttle

    def set_throttle(self, throttle):
        self.throttle = throttle
        Qt.QMetaObject.invokeMethod(self._throttle_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.throttle)))
        self.blocks_throttle_0.set_sample_rate(self.rri_samp_rate*self.throttle)
        self.blocks_throttle_0_0.set_sample_rate(self.rri_samp_rate*self.throttle)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.lpf_bw, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.lpf_bw, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.lpf_bw, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.lpf_bw, 1e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate / self.decim)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate / self.decim)

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--avg-len", dest="avg_len", type=eng_float, default="1.024k",
        help="Set avg_len [default=%(default)r]")
    parser.add_argument(
        "--decim", dest="decim", type=intx, default=16,
        help="Set decim [default=%(default)r]")
    parser.add_argument(
        "--lpf-bw", dest="lpf_bw", type=eng_float, default="1.5k",
        help="Set lpf_bw [default=%(default)r]")
    parser.add_argument(
        "--nfft", dest="nfft", type=intx, default=2048,
        help="Set nfft [default=%(default)r]")
    return parser


def main(top_block_cls=rri_phase_1, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(avg_len=options.avg_len, decim=options.decim, lpf_bw=options.lpf_bw, nfft=options.nfft)

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
