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
from gnuradio import blocks
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
        self.samp_rate = samp_rate = 500e3
        self.rx_freq = rx_freq = 20e6
        self.ns_ant_label = ns_ant_label = 'North/South'
        self.ew_ant_label = ew_ant_label = 'East/West'

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
        self.main_tab.addTab(self.main_tab_widget_1, 'Polarized')
        self.main_tab_widget_2 = Qt.QWidget()
        self.main_tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_2)
        self.main_tab_grid_layout_2 = Qt.QGridLayout()
        self.main_tab_layout_2.addLayout(self.main_tab_grid_layout_2)
        self.main_tab.addTab(self.main_tab_widget_2, 'Audio')
        self.main_tab_widget_3 = Qt.QWidget()
        self.main_tab_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_3)
        self.main_tab_grid_layout_3 = Qt.QGridLayout()
        self.main_tab_layout_3.addLayout(self.main_tab_grid_layout_3)
        self.main_tab.addTab(self.main_tab_widget_3, 'Power')
        self.top_grid_layout.addWidget(self.main_tab, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel('samp_rate' + ": "))
        self._samp_rate_line_edit = Qt.QLineEdit(str(self.samp_rate))
        self._samp_rate_tool_bar.addWidget(self._samp_rate_line_edit)
        self._samp_rate_line_edit.returnPressed.connect(
            lambda: self.set_samp_rate(eng_notation.str_to_num(str(self._samp_rate_line_edit.text()))))
        self.main_tab_grid_layout_0.addWidget(self._samp_rate_tool_bar, 5, 0, 1, 2)
        for r in range(5, 6):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self._rx_freq_tool_bar = Qt.QToolBar(self)
        self._rx_freq_tool_bar.addWidget(Qt.QLabel('Freq [Hz]' + ": "))
        self._rx_freq_line_edit = Qt.QLineEdit(str(self.rx_freq))
        self._rx_freq_tool_bar.addWidget(self._rx_freq_line_edit)
        self._rx_freq_line_edit.returnPressed.connect(
            lambda: self.set_rx_freq(eng_notation.str_to_num(str(self._rx_freq_line_edit.text()))))
        self.main_tab_grid_layout_0.addWidget(self._rx_freq_tool_bar, 5, 2, 1, 2)
        for r in range(5, 6):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 4):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
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
        self.uhd_usrp_source_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(rx_freq, samp_rate/2), 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(rx_freq, samp_rate/2), 1)
        self.uhd_usrp_source_0.set_gain(0, 1)
        self.uhd_usrp_source_0.set_antenna('RX2', 1)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
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
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_1_0_win, 4, 4, 2, 4)
        for r in range(4, 6):
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
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_win, 6, 4, 2, 4)
        for r in range(6, 8):
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
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_0_win, 2, 4, 2, 4)
        for r in range(2, 4):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
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
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_win, 0, 4, 2, 4)
        for r in range(0, 2):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(4, 8):
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



        labels = ['N/S', 'E/W', '', '', '',
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
        self.main_tab_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 4, 4)
        for r in range(0, 4):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
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
        self.fosphor_qt_sink_c_0_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(rx_freq, samp_rate)
        self._fosphor_qt_sink_c_0_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._fosphor_qt_sink_c_0_0_win, 1, 4, 3, 4)
        for r in range(1, 4):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(rx_freq, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._fosphor_qt_sink_c_0_win, 1, 0, 3, 4)
        for r in range(1, 4):
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
        self.blocks_multiply_const_vxx_1_0_1 = blocks.multiply_const_cc(complex(0,1))
        self.blocks_multiply_const_vxx_1_0_0_0 = blocks.multiply_const_cc(complex(0,-1))
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_0, 2))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_waterfall_sink_x_0_1_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.qtgui_freq_sink_x_0, 3))
        self.connect((self.blocks_add_xx_0_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_multiply_const_vxx_1_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_multiply_const_vxx_1_0_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.fosphor_qt_sink_c_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.fosphor_qt_sink_c_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.qtgui_waterfall_sink_x_0_0, 0))


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
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_1_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/2), 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/2), 1)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        Qt.QMetaObject.invokeMethod(self._rx_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_freq)))
        self.fosphor_qt_sink_c_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0_0_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_1_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/2), 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/2), 1)

    def get_ns_ant_label(self):
        return self.ns_ant_label

    def set_ns_ant_label(self, ns_ant_label):
        self.ns_ant_label = ns_ant_label
        Qt.QMetaObject.invokeMethod(self._ns_ant_label_label, "setText", Qt.Q_ARG("QString", self.ns_ant_label))

    def get_ew_ant_label(self):
        return self.ew_ant_label

    def set_ew_ant_label(self, ew_ant_label):
        self.ew_ant_label = ew_ant_label
        Qt.QMetaObject.invokeMethod(self._ew_ant_label_label, "setText", Qt.Q_ARG("QString", self.ew_ant_label))





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
