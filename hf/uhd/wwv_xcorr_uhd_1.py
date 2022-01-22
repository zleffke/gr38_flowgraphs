#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: WWV Cross Correlation Monitor
# Author: Zach Leffke, KJ4QLP
# Copyright: MIT
# Description: WWV Polarization Discrimination, V1
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
from gnuradio import fosphor
from gnuradio.fft import window
from datetime import datetime as dt; import string; import math; import numpy as np
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time

from gnuradio import qtgui

class wwv_xcorr_uhd_1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "WWV Cross Correlation Monitor")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("WWV Cross Correlation Monitor")
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

        self.settings = Qt.QSettings("GNU Radio", "wwv_xcorr_uhd_1")

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
        self.samp_rate = samp_rate = 0.5e6
        self.rx_freq = rx_freq = 15e6
        self.ns_ant_label = ns_ant_label = 'North/South'
        self.lpf_cut = lpf_cut = 5e3
        self.ew_ant_label = ew_ant_label = 'East/West'
        self.decim_1 = decim_1 = 50
        self.avg_len_pwr = avg_len_pwr = 10000.0
        self.avg_len = avg_len = 100

        ##################################################
        # Blocks
        ##################################################
        self.main_tab = Qt.QTabWidget()
        self.main_tab_widget_0 = Qt.QWidget()
        self.main_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_0)
        self.main_tab_grid_layout_0 = Qt.QGridLayout()
        self.main_tab_layout_0.addLayout(self.main_tab_grid_layout_0)
        self.main_tab.addTab(self.main_tab_widget_0, 'Channel')
        self.main_tab_widget_1 = Qt.QWidget()
        self.main_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_1)
        self.main_tab_grid_layout_1 = Qt.QGridLayout()
        self.main_tab_layout_1.addLayout(self.main_tab_grid_layout_1)
        self.main_tab.addTab(self.main_tab_widget_1, 'Filter + Resamp')
        self.main_tab_widget_2 = Qt.QWidget()
        self.main_tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_2)
        self.main_tab_grid_layout_2 = Qt.QGridLayout()
        self.main_tab_layout_2.addLayout(self.main_tab_grid_layout_2)
        self.main_tab.addTab(self.main_tab_widget_2, 'Phase')
        self.main_tab_widget_3 = Qt.QWidget()
        self.main_tab_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_3)
        self.main_tab_grid_layout_3 = Qt.QGridLayout()
        self.main_tab_layout_3.addLayout(self.main_tab_grid_layout_3)
        self.main_tab.addTab(self.main_tab_widget_3, 'Power')
        self.top_grid_layout.addWidget(self.main_tab, 0, 0, 4, 4)
        for r in range(0, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel('samp_rate' + ": "))
        self._samp_rate_line_edit = Qt.QLineEdit(str(self.samp_rate))
        self._samp_rate_tool_bar.addWidget(self._samp_rate_line_edit)
        self._samp_rate_line_edit.returnPressed.connect(
            lambda: self.set_samp_rate(eng_notation.str_to_num(str(self._samp_rate_line_edit.text()))))
        self.top_grid_layout.addWidget(self._samp_rate_tool_bar, 5, 0, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_freq_tool_bar = Qt.QToolBar(self)
        self._rx_freq_tool_bar.addWidget(Qt.QLabel('Freq [Hz]' + ": "))
        self._rx_freq_line_edit = Qt.QLineEdit(str(self.rx_freq))
        self._rx_freq_tool_bar.addWidget(self._rx_freq_line_edit)
        self._rx_freq_line_edit.returnPressed.connect(
            lambda: self.set_rx_freq(eng_notation.str_to_num(str(self._rx_freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._rx_freq_tool_bar, 5, 2, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._lpf_cut_tool_bar = Qt.QToolBar(self)
        self._lpf_cut_tool_bar.addWidget(Qt.QLabel('Freq [Hz]' + ": "))
        self._lpf_cut_line_edit = Qt.QLineEdit(str(self.lpf_cut))
        self._lpf_cut_tool_bar.addWidget(self._lpf_cut_line_edit)
        self._lpf_cut_line_edit.returnPressed.connect(
            lambda: self.set_lpf_cut(eng_notation.str_to_num(str(self._lpf_cut_line_edit.text()))))
        self.main_tab_grid_layout_1.addWidget(self._lpf_cut_tool_bar, 8, 0, 1, 2)
        for r in range(8, 9):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 2):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self._avg_len_pwr_tool_bar = Qt.QToolBar(self)
        self._avg_len_pwr_tool_bar.addWidget(Qt.QLabel('avg_len_pwr' + ": "))
        self._avg_len_pwr_line_edit = Qt.QLineEdit(str(self.avg_len_pwr))
        self._avg_len_pwr_tool_bar.addWidget(self._avg_len_pwr_line_edit)
        self._avg_len_pwr_line_edit.returnPressed.connect(
            lambda: self.set_avg_len_pwr(eng_notation.str_to_num(str(self._avg_len_pwr_line_edit.text()))))
        self.main_tab_grid_layout_3.addWidget(self._avg_len_pwr_tool_bar, 2, 2, 1, 2)
        for r in range(2, 3):
            self.main_tab_grid_layout_3.setRowStretch(r, 1)
        for c in range(2, 4):
            self.main_tab_grid_layout_3.setColumnStretch(c, 1)
        self._avg_len_tool_bar = Qt.QToolBar(self)
        self._avg_len_tool_bar.addWidget(Qt.QLabel('avg_len' + ": "))
        self._avg_len_line_edit = Qt.QLineEdit(str(self.avg_len))
        self._avg_len_tool_bar.addWidget(self._avg_len_line_edit)
        self._avg_len_line_edit.returnPressed.connect(
            lambda: self.set_avg_len(eng_notation.str_to_num(str(self._avg_len_line_edit.text()))))
        self.main_tab_grid_layout_2.addWidget(self._avg_len_tool_bar, 5, 0, 1, 2)
        for r in range(5, 6):
            self.main_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 2):
            self.main_tab_grid_layout_2.setColumnStretch(c, 1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("addr=10.41.1.11", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source_0.set_subdev_spec('A:A A:B', 0)
        self.uhd_usrp_source_0.set_time_source('gpsdo', 0)
        self.uhd_usrp_source_0.set_clock_source('internal', 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(rx_freq, samp_rate/4), 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(rx_freq, samp_rate/4), 1)
        self.uhd_usrp_source_0.set_gain(0, 1)
        self.uhd_usrp_source_0.set_antenna('RX2', 1)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim_1,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim_1,
                taps=None,
                fractional_bw=None)
        self.qtgui_waterfall_sink_x_0_1_0_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate / decim_1, #bw
            "RHCP", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_1_0_0.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0_1_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_1_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_1_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_1_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_1_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_1_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_1_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_1_0_0_win, 4, 4, 2, 4)
        for r in range(4, 6):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_1_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate, #bw
            "RHCP", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_1_0.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0_1_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_1_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_1_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_1_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_1_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_1_0_win, 4, 4, 1, 2)
        for r in range(4, 5):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 6):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_1 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate / decim_1, #bw
            "N/S", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_1.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_1.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_1_win, 0, 4, 2, 4)
        for r in range(0, 2):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_0_0_0_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate / decim_1, #bw
            "LHCP", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_0_win, 6, 4, 2, 4)
        for r in range(6, 8):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_0_0_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate, #bw
            "LHCP", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0_0.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_win, 4, 6, 1, 2)
        for r in range(4, 5):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 8):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_0_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate / decim_1, #bw
            "E/W", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_0_0_win, 2, 4, 2, 4)
        for r in range(2, 4):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate, #bw
            "E/W", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_0_win, 3, 6, 1, 2)
        for r in range(3, 4):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 8):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate, #bw
            "N/S", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 3, 4, 1, 2)
        for r in range(3, 4):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 6):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate / decim_1, #samp_rate
            "", #name
            4 #number of inputs
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.1)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_1.enable_grid(True)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)


        labels = ['N/S', 'E/W', 'RHCP', 'LHCP', '',
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
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_3.addWidget(self._qtgui_time_sink_x_0_1_win, 0, 0, 2, 4)
        for r in range(0, 2):
            self.main_tab_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            1024*8, #size
            samp_rate, #samp_rate
            "Original", #name
            3 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.010)
        self.qtgui_time_sink_x_0_0.set_y_axis(-360, 360)

        self.qtgui_time_sink_x_0_0.set_y_label('Phase', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['NS', 'EW', 'NS-EW', '', '',
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


        for i in range(3):
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
        self.main_tab_grid_layout_2.addWidget(self._qtgui_time_sink_x_0_0_win, 2, 0, 2, 4)
        for r in range(2, 4):
            self.main_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024 * 32, #size
            samp_rate / decim_1, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.010)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


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


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_2.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 2, 2)
        for r in range(0, 2):
            self.main_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 2):
            self.main_tab_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_VERT,
            4
        )
        self.qtgui_number_sink_0_0.set_update_time(0.010)
        self.qtgui_number_sink_0_0.set_title('RSSI')

        labels = ["N/S", "E/W", "RHCP", "LHCP", '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("blue", "red"), ("blue", "red"), ("blue", "red"), ("blue", "red"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(4):
            self.qtgui_number_sink_0_0.set_min(i, -40)
            self.qtgui_number_sink_0_0.set_max(i, -140)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_3.addWidget(self._qtgui_number_sink_0_0_win, 2, 0, 2, 2)
        for r in range(2, 4):
            self.main_tab_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 2):
            self.main_tab_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_1_0 = qtgui.histogram_sink_f(
            100,
            2000,
            -360,
            360,
            "Phase",
            1
        )

        self.qtgui_histogram_sink_x_1_0.set_update_time(0.10)
        self.qtgui_histogram_sink_x_1_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_1_0.enable_accumulate(True)
        self.qtgui_histogram_sink_x_1_0.enable_grid(True)
        self.qtgui_histogram_sink_x_1_0.enable_axis_labels(True)


        labels = ['RHCP', 'LHCP', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_1_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_2.addWidget(self._qtgui_histogram_sink_x_1_0_win, 0, 2, 2, 2)
        for r in range(0, 2):
            self.main_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 4):
            self.main_tab_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            4096, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate / decim_1, #bw
            "Filtered and Resampled", #name
            4
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.010)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)



        labels = ['N/S', 'E/W', 'RHCP', 'LHCP', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(4):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_win, 0, 0, 4, 4)
        for r in range(0, 4):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate, #bw
            "", #name
            4
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.010)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['N/S', 'E/W', 'RHCP', 'LHCP', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(4):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 3, 0, 2, 4)
        for r in range(3, 5):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self._ns_ant_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._ns_ant_label_formatter = None
        else:
            self._ns_ant_label_formatter = lambda x: str(x)

        self._ns_ant_label_tool_bar.addWidget(Qt.QLabel('Antenna' + ": "))
        self._ns_ant_label_label = Qt.QLabel(str(self._ns_ant_label_formatter(self.ns_ant_label)))
        self._ns_ant_label_tool_bar.addWidget(self._ns_ant_label_label)
        self.main_tab_grid_layout_0.addWidget(self._ns_ant_label_tool_bar, 0, 0, 1, 4)
        for r in range(0, 1):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.low_pass_filter_1 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate / decim_1,
                lpf_cut,
                1e3,
                firdes.WIN_BLACKMAN,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate / decim_1,
                lpf_cut,
                .1e3,
                firdes.WIN_BLACKMAN,
                6.76))
        self.fosphor_qt_sink_c_0_1 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_1.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_1.set_frequency_range(rx_freq, samp_rate / decim_1)
        self._fosphor_qt_sink_c_0_1_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_1.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_1.addWidget(self._fosphor_qt_sink_c_0_1_win, 4, 0, 4, 4)
        for r in range(4, 8):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.fosphor_qt_sink_c_0_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(rx_freq, samp_rate)
        self._fosphor_qt_sink_c_0_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._fosphor_qt_sink_c_0_0_win, 1, 4, 2, 4)
        for r in range(1, 3):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(rx_freq, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._fosphor_qt_sink_c_0_win, 1, 0, 2, 4)
        for r in range(1, 3):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self._ew_ant_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._ew_ant_label_formatter = None
        else:
            self._ew_ant_label_formatter = lambda x: str(x)

        self._ew_ant_label_tool_bar.addWidget(Qt.QLabel('Antenna' + ": "))
        self._ew_ant_label_label = Qt.QLabel(str(self._ew_ant_label_formatter(self.ew_ant_label)))
        self._ew_ant_label_tool_bar.addWidget(self._ew_ant_label_label)
        self.main_tab_grid_layout_0.addWidget(self._ew_ant_label_tool_bar, 0, 4, 1, 4)
        for r in range(0, 1):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.blocks_sub_xx_1_0 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_nlog10_ff_0_1 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_nlog10_ff_0_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_multiply_const_vxx_1_0_3 = blocks.multiply_const_ff(1/avg_len_pwr)
        self.blocks_multiply_const_vxx_1_0_2 = blocks.multiply_const_ff(180.0/math.pi)
        self.blocks_multiply_const_vxx_1_0_1_0 = blocks.multiply_const_cc(complex(0,-1))
        self.blocks_multiply_const_vxx_1_0_1 = blocks.multiply_const_cc(complex(0,-1))
        self.blocks_multiply_const_vxx_1_0_0_2_0 = blocks.multiply_const_ff(180.0/math.pi)
        self.blocks_multiply_const_vxx_1_0_0_2 = blocks.multiply_const_ff(180.0/math.pi)
        self.blocks_multiply_const_vxx_1_0_0_1 = blocks.multiply_const_ff(1/avg_len_pwr)
        self.blocks_multiply_const_vxx_1_0_0_0_0 = blocks.multiply_const_cc(complex(0,1))
        self.blocks_multiply_const_vxx_1_0_0_0 = blocks.multiply_const_cc(complex(0,1))
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_ff(1/avg_len_pwr)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_ff(1/avg_len_pwr)
        self.blocks_moving_average_xx_0_2 = blocks.moving_average_ff(int(avg_len_pwr), 1/avg_len_pwr, 4000, 1)
        self.blocks_moving_average_xx_0_1 = blocks.moving_average_ff(int(avg_len), 1.0/avg_len, 4000, 1)
        self.blocks_moving_average_xx_0_0_1 = blocks.moving_average_ff(int(avg_len_pwr), 1/avg_len_pwr, 4000, 1)
        self.blocks_moving_average_xx_0_0_0 = blocks.moving_average_ff(int(avg_len), 1.0/avg_len, 4000, 1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(int(avg_len_pwr), 1/avg_len_pwr, 4000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int(avg_len_pwr), 1/avg_len_pwr, 4000, 1)
        self.blocks_complex_to_mag_squared_0_1 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_arg_0_0_0_2 = blocks.complex_to_arg(1)
        self.blocks_complex_to_arg_0_0_0_0_1 = blocks.complex_to_arg(1)
        self.blocks_add_xx_0_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_0, 2))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_waterfall_sink_x_0_1_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.qtgui_freq_sink_x_0, 3))
        self.connect((self.blocks_add_xx_0_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0, 0))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.blocks_complex_to_arg_0_0_0_0_1, 0))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.blocks_complex_to_mag_squared_0_0_0, 0))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.qtgui_freq_sink_x_0_0, 3))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0_0, 0))
        self.connect((self.blocks_add_xx_0_1, 0), (self.blocks_complex_to_arg_0_0_0_2, 0))
        self.connect((self.blocks_add_xx_0_1, 0), (self.blocks_complex_to_mag_squared_0_1, 0))
        self.connect((self.blocks_add_xx_0_1, 0), (self.qtgui_freq_sink_x_0_0, 2))
        self.connect((self.blocks_add_xx_0_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_add_xx_0_1, 0), (self.qtgui_waterfall_sink_x_0_1_0_0, 0))
        self.connect((self.blocks_complex_to_arg_0_0_0_0_1, 0), (self.blocks_multiply_const_vxx_1_0_0_2_0, 0))
        self.connect((self.blocks_complex_to_arg_0_0_0_0_1, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_complex_to_arg_0_0_0_2, 0), (self.blocks_multiply_const_vxx_1_0_0_2, 0))
        self.connect((self.blocks_complex_to_arg_0_0_0_2, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0_0, 0), (self.blocks_moving_average_xx_0_0_1, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_1, 0), (self.blocks_moving_average_xx_0_2, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_multiply_const_vxx_1_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0_0, 0), (self.blocks_sub_xx_1_0, 1))
        self.connect((self.blocks_moving_average_xx_0_0_1, 0), (self.blocks_multiply_const_vxx_1_0_0_1, 0))
        self.connect((self.blocks_moving_average_xx_0_1, 0), (self.blocks_sub_xx_1_0, 0))
        self.connect((self.blocks_moving_average_xx_0_2, 0), (self.blocks_multiply_const_vxx_1_0_3, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0_0, 0), (self.blocks_add_xx_0_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_1, 0), (self.blocks_nlog10_ff_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_2, 0), (self.blocks_moving_average_xx_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_2, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_2_0, 0), (self.blocks_moving_average_xx_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_2_0, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_1_0, 0), (self.blocks_add_xx_0_1, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_2, 0), (self.qtgui_time_sink_x_0_0, 2))
        self.connect((self.blocks_multiply_const_vxx_1_0_3, 0), (self.blocks_nlog10_ff_0_1, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.qtgui_number_sink_0_0, 1))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.qtgui_time_sink_x_0_1, 1))
        self.connect((self.blocks_nlog10_ff_0_0_0, 0), (self.qtgui_number_sink_0_0, 3))
        self.connect((self.blocks_nlog10_ff_0_0_0, 0), (self.qtgui_time_sink_x_0_1, 3))
        self.connect((self.blocks_nlog10_ff_0_1, 0), (self.qtgui_number_sink_0_0, 2))
        self.connect((self.blocks_nlog10_ff_0_1, 0), (self.qtgui_time_sink_x_0_1, 2))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_const_vxx_1_0_2, 0))
        self.connect((self.blocks_sub_xx_1_0, 0), (self.qtgui_histogram_sink_x_1_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_add_xx_0_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_add_xx_0_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.fosphor_qt_sink_c_0_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_0_1, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_multiply_const_vxx_1_0_0_0_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_multiply_const_vxx_1_0_1_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.qtgui_freq_sink_x_0_0, 1))
        self.connect((self.low_pass_filter_1, 0), (self.qtgui_waterfall_sink_x_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.low_pass_filter_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_multiply_const_vxx_1_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_multiply_const_vxx_1_0_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.fosphor_qt_sink_c_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.fosphor_qt_sink_c_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.qtgui_waterfall_sink_x_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.rational_resampler_xxx_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "wwv_xcorr_uhd_1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        Qt.QMetaObject.invokeMethod(self._samp_rate_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.samp_rate)))
        self.fosphor_qt_sink_c_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.fosphor_qt_sink_c_0_1.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate / self.decim_1, self.lpf_cut, .1e3, firdes.WIN_BLACKMAN, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate / self.decim_1, self.lpf_cut, 1e3, firdes.WIN_BLACKMAN, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate / self.decim_1)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_1.set_samp_rate(self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_1.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_1_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_1_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/4), 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/4), 1)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        Qt.QMetaObject.invokeMethod(self._rx_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_freq)))
        self.fosphor_qt_sink_c_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.fosphor_qt_sink_c_0_1.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_1.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_1_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_1_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/4), 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/4), 1)

    def get_ns_ant_label(self):
        return self.ns_ant_label

    def set_ns_ant_label(self, ns_ant_label):
        self.ns_ant_label = ns_ant_label
        Qt.QMetaObject.invokeMethod(self._ns_ant_label_label, "setText", Qt.Q_ARG("QString", self.ns_ant_label))

    def get_lpf_cut(self):
        return self.lpf_cut

    def set_lpf_cut(self, lpf_cut):
        self.lpf_cut = lpf_cut
        Qt.QMetaObject.invokeMethod(self._lpf_cut_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.lpf_cut)))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate / self.decim_1, self.lpf_cut, .1e3, firdes.WIN_BLACKMAN, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate / self.decim_1, self.lpf_cut, 1e3, firdes.WIN_BLACKMAN, 6.76))

    def get_ew_ant_label(self):
        return self.ew_ant_label

    def set_ew_ant_label(self, ew_ant_label):
        self.ew_ant_label = ew_ant_label
        Qt.QMetaObject.invokeMethod(self._ew_ant_label_label, "setText", Qt.Q_ARG("QString", self.ew_ant_label))

    def get_decim_1(self):
        return self.decim_1

    def set_decim_1(self, decim_1):
        self.decim_1 = decim_1
        self.fosphor_qt_sink_c_0_1.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate / self.decim_1, self.lpf_cut, .1e3, firdes.WIN_BLACKMAN, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate / self.decim_1, self.lpf_cut, 1e3, firdes.WIN_BLACKMAN, 6.76))
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate / self.decim_1)
        self.qtgui_time_sink_x_0_1.set_samp_rate(self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_1.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)
        self.qtgui_waterfall_sink_x_0_1_0_0.set_frequency_range(self.rx_freq, self.samp_rate / self.decim_1)

    def get_avg_len_pwr(self):
        return self.avg_len_pwr

    def set_avg_len_pwr(self, avg_len_pwr):
        self.avg_len_pwr = avg_len_pwr
        Qt.QMetaObject.invokeMethod(self._avg_len_pwr_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.avg_len_pwr)))
        self.blocks_moving_average_xx_0.set_length_and_scale(int(self.avg_len_pwr), 1/self.avg_len_pwr)
        self.blocks_moving_average_xx_0_0.set_length_and_scale(int(self.avg_len_pwr), 1/self.avg_len_pwr)
        self.blocks_moving_average_xx_0_0_1.set_length_and_scale(int(self.avg_len_pwr), 1/self.avg_len_pwr)
        self.blocks_moving_average_xx_0_2.set_length_and_scale(int(self.avg_len_pwr), 1/self.avg_len_pwr)
        self.blocks_multiply_const_vxx_1_0.set_k(1/self.avg_len_pwr)
        self.blocks_multiply_const_vxx_1_0_0.set_k(1/self.avg_len_pwr)
        self.blocks_multiply_const_vxx_1_0_0_1.set_k(1/self.avg_len_pwr)
        self.blocks_multiply_const_vxx_1_0_3.set_k(1/self.avg_len_pwr)

    def get_avg_len(self):
        return self.avg_len

    def set_avg_len(self, avg_len):
        self.avg_len = avg_len
        Qt.QMetaObject.invokeMethod(self._avg_len_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.avg_len)))
        self.blocks_moving_average_xx_0_0_0.set_length_and_scale(int(self.avg_len), 1.0/self.avg_len)
        self.blocks_moving_average_xx_0_1.set_length_and_scale(int(self.avg_len), 1.0/self.avg_len)





def main(top_block_cls=wwv_xcorr_uhd_1, options=None):

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
