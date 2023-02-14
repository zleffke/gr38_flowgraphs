#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: VCC Burst TX/RX, 9600 Baud GMSK, AX.25, w/ PTT
# Author: Zach Leffke, KJ4QLP
# Description: VCC Burst TX/RX, 9600 Baud GMSK, AX.25
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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from datetime import datetime as dt; import string; import math
from fsk_burst_detector import fsk_burst_detector  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import fhss_utils
import gr_sigmf
import pdu_utils

from gnuradio import qtgui

class burst_rx_gmsk9600_ax25_playback(gr.top_block, Qt.QWidget):

    def __init__(self, burst_width=int(20e3), chan_cutoff=12e3, chan_trans_width=1e3, fft_size=int(512), hist_time=0.075, lookahead_time=0.01, max_burst_time=0.25, min_burst_time=0.01, post_burst_time=0.5, pre_burst_time=0.075):
        gr.top_block.__init__(self, "VCC Burst TX/RX, 9600 Baud GMSK, AX.25, w/ PTT")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("VCC Burst TX/RX, 9600 Baud GMSK, AX.25, w/ PTT")
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

        self.settings = Qt.QSettings("GNU Radio", "burst_rx_gmsk9600_ax25_playback")

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
        self.burst_width = burst_width
        self.chan_cutoff = chan_cutoff
        self.chan_trans_width = chan_trans_width
        self.fft_size = fft_size
        self.hist_time = hist_time
        self.lookahead_time = lookahead_time
        self.max_burst_time = max_burst_time
        self.min_burst_time = min_burst_time
        self.post_burst_time = post_burst_time
        self.pre_burst_time = pre_burst_time

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = float(250e3)
        self.ts_str = ts_str = dt.strftime(dt.utcnow(), "%Y%m%d_%H%M%S" )
        self.interp_2 = interp_2 = 1
        self.interp = interp = 48
        self.gs_id = gs_id = "VTGS"
        self.decim_2 = decim_2 = 2
        self.decim = decim = int(samp_rate/2000)
        self.fn = fn = "VCC_{:s}_{:s}".format(gs_id, ts_str)
        self.chan_samp_rate = chan_samp_rate = int(samp_rate / decim*interp / decim_2 * interp_2)
        self.trigger_thresh = trigger_thresh = 15
        self.rx_offset = rx_offset = samp_rate/2.0
        self.rx_gain = rx_gain = 20
        self.rx_freq = rx_freq = 401.08e6
        self.rate_factor = rate_factor = 1
        self.fsk_dev = fsk_dev = 10000
        self.fp = fp = "/vtgs/captures/vcc/{:s}".format(fn)
        self.fine_offset = fine_offset = 0
        self.decim_taps = decim_taps = firdes.low_pass(1.0, chan_samp_rate, chan_cutoff,chan_trans_width, firdes.WIN_HAMMING, 6.76)
        self.chan_offset = chan_offset = -40e3
        self.chan_filt_trans = chan_filt_trans = 1000
        self.chan_filt_cutoff = chan_filt_cutoff = 24000

        ##################################################
        # Blocks
        ##################################################
        self.main_tab = Qt.QTabWidget()
        self.main_tab_widget_0 = Qt.QWidget()
        self.main_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_0)
        self.main_tab_grid_layout_0 = Qt.QGridLayout()
        self.main_tab_layout_0.addLayout(self.main_tab_grid_layout_0)
        self.main_tab.addTab(self.main_tab_widget_0, 'Full Band')
        self.main_tab_widget_1 = Qt.QWidget()
        self.main_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_1)
        self.main_tab_grid_layout_1 = Qt.QGridLayout()
        self.main_tab_layout_1.addLayout(self.main_tab_grid_layout_1)
        self.main_tab.addTab(self.main_tab_widget_1, 'RX Channel')
        self.main_tab_widget_2 = Qt.QWidget()
        self.main_tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_2)
        self.main_tab_grid_layout_2 = Qt.QGridLayout()
        self.main_tab_layout_2.addLayout(self.main_tab_grid_layout_2)
        self.main_tab.addTab(self.main_tab_widget_2, 'Burst')
        self.top_grid_layout.addWidget(self.main_tab, 0, 0, 2, 8)
        for r in range(0, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._trigger_thresh_tool_bar = Qt.QToolBar(self)
        self._trigger_thresh_tool_bar.addWidget(Qt.QLabel('Trigger Thresh' + ": "))
        self._trigger_thresh_line_edit = Qt.QLineEdit(str(self.trigger_thresh))
        self._trigger_thresh_tool_bar.addWidget(self._trigger_thresh_line_edit)
        self._trigger_thresh_line_edit.returnPressed.connect(
            lambda: self.set_trigger_thresh(eng_notation.str_to_num(str(self._trigger_thresh_line_edit.text()))))
        self.main_tab_grid_layout_1.addWidget(self._trigger_thresh_tool_bar, 4, 0, 1, 2)
        for r in range(4, 5):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 2):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self._rx_freq_tool_bar = Qt.QToolBar(self)
        self._rx_freq_tool_bar.addWidget(Qt.QLabel('RX Freq' + ": "))
        self._rx_freq_line_edit = Qt.QLineEdit(str(self.rx_freq))
        self._rx_freq_tool_bar.addWidget(self._rx_freq_line_edit)
        self._rx_freq_line_edit.returnPressed.connect(
            lambda: self.set_rx_freq(eng_notation.str_to_num(str(self._rx_freq_line_edit.text()))))
        self.main_tab_grid_layout_0.addWidget(self._rx_freq_tool_bar, 4, 0, 1, 2)
        for r in range(4, 5):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self._rate_factor_tool_bar = Qt.QToolBar(self)
        self._rate_factor_tool_bar.addWidget(Qt.QLabel('rate_factor' + ": "))
        self._rate_factor_line_edit = Qt.QLineEdit(str(self.rate_factor))
        self._rate_factor_tool_bar.addWidget(self._rate_factor_line_edit)
        self._rate_factor_line_edit.returnPressed.connect(
            lambda: self.set_rate_factor(eng_notation.str_to_num(str(self._rate_factor_line_edit.text()))))
        self.top_grid_layout.addWidget(self._rate_factor_tool_bar, 2, 0, 1, 8)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._fine_offset_tool_bar = Qt.QToolBar(self)
        self._fine_offset_tool_bar.addWidget(Qt.QLabel('fine_offset' + ": "))
        self._fine_offset_line_edit = Qt.QLineEdit(str(self.fine_offset))
        self._fine_offset_tool_bar.addWidget(self._fine_offset_line_edit)
        self._fine_offset_line_edit.returnPressed.connect(
            lambda: self.set_fine_offset(eng_notation.str_to_num(str(self._fine_offset_line_edit.text()))))
        self.top_layout.addWidget(self._fine_offset_tool_bar)
        self._chan_offset_tool_bar = Qt.QToolBar(self)
        self._chan_offset_tool_bar.addWidget(Qt.QLabel('Chan Offset' + ": "))
        self._chan_offset_line_edit = Qt.QLineEdit(str(self.chan_offset))
        self._chan_offset_tool_bar.addWidget(self._chan_offset_line_edit)
        self._chan_offset_line_edit.returnPressed.connect(
            lambda: self.set_chan_offset(eng_notation.str_to_num(str(self._chan_offset_line_edit.text()))))
        self.main_tab_grid_layout_1.addWidget(self._chan_offset_tool_bar, 4, 2, 1, 2)
        for r in range(4, 5):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 4):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.sigmf_source_0 = gr_sigmf.source('/home/zleffke/captures/VCC_VTGS_20191123_060818.sigmf-data', "cf32" + ("_le" if sys.byteorder == "little" else "_be"), False)
        self._rx_gain_tool_bar = Qt.QToolBar(self)
        self._rx_gain_tool_bar.addWidget(Qt.QLabel('RX Gain' + ": "))
        self._rx_gain_line_edit = Qt.QLineEdit(str(self.rx_gain))
        self._rx_gain_tool_bar.addWidget(self._rx_gain_line_edit)
        self._rx_gain_line_edit.returnPressed.connect(
            lambda: self.set_rx_gain(eng_notation.str_to_num(str(self._rx_gain_line_edit.text()))))
        self.main_tab_grid_layout_0.addWidget(self._rx_gain_tool_bar, 4, 2, 1, 2)
        for r in range(4, 5):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 4):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.rational_resampler_xxx_1_0 = filter.rational_resampler_ccc(
                interpolation=interp_2,
                decimation=decim_2,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=interp,
                decimation=decim,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=2,
                taps=None,
                fractional_bw=None)
        self.qtgui_waterfall_sink_x_0_1 = qtgui.waterfall_sink_c(
            128, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            chan_samp_rate, #bw
            "Burst Spectrogram", #name
            0 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_1.set_update_time(0.005)
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
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_1_win, 2, 4, 2, 4)
        for r in range(2, 4):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate / decim*interp / decim_2 * interp_2, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(True)
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

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-50, 50)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_0_win, 2, 0, 2, 4)
        for r in range(2, 4):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.0010)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
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
        self.main_tab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 1, 0, 1, 8)
        for r in range(1, 2):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 8):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            1024, #size
            chan_samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0.005, 0, "burst_start")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


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
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_2.addWidget(self._qtgui_time_sink_x_1_win, 0, 4, 2, 4)
        for r in range(0, 2):
            self.main_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Threshold", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.010)
        self.qtgui_time_sink_x_0.set_y_axis(-10, 10)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


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


        for i in range(2):
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
        self.main_tab_grid_layout_2.addWidget(self._qtgui_time_sink_x_0_win, 2, 4, 1, 4)
        for r in range(2, 3):
            self.main_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(4, 8):
            self.main_tab_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1_0_1 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            rx_freq, #fc
            samp_rate, #bw
            "VCC RX Spectrum", #name
            1
        )
        self.qtgui_freq_sink_x_1_0_1.set_update_time(0.0010)
        self.qtgui_freq_sink_x_1_0_1.set_y_axis(-130, -60)
        self.qtgui_freq_sink_x_1_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_0_1.enable_grid(True)
        self.qtgui_freq_sink_x_1_0_1.set_fft_average(0.2)
        self.qtgui_freq_sink_x_1_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_0_1.enable_control_panel(False)

        self.qtgui_freq_sink_x_1_0_1.disable_legend()


        labels = ['pre-d', 'agc_filt', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_0_1.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_0.addWidget(self._qtgui_freq_sink_x_1_0_1_win, 0, 0, 1, 8)
        for r in range(0, 1):
            self.main_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 8):
            self.main_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1_0 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate / decim*interp / decim_2 * interp_2, #bw
            "Channel Spectrum", #name
            1
        )
        self.qtgui_freq_sink_x_1_0.set_update_time(0.0010)
        self.qtgui_freq_sink_x_1_0.set_y_axis(-50, 50)
        self.qtgui_freq_sink_x_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_0.enable_grid(True)
        self.qtgui_freq_sink_x_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_0.enable_control_panel(False)

        self.qtgui_freq_sink_x_1_0.disable_legend()


        labels = ['pre-d', 'agc_filt', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.main_tab_grid_layout_1.addWidget(self._qtgui_freq_sink_x_1_0_win, 0, 0, 2, 4)
        for r in range(0, 2):
            self.main_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 4):
            self.main_tab_grid_layout_1.setColumnStretch(c, 1)
        self.pdu_utils_pdu_split_0 = pdu_utils.pdu_split(False)
        self.pdu_utils_pdu_fine_time_measure_0 = pdu_utils.pdu_fine_time_measure(pre_burst_time, post_burst_time, 10, 15)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate / decim *interp,
                chan_filt_cutoff,
                chan_filt_trans,
                firdes.WIN_HAMMING,
                6.76))
        self.fsk_burst_detector_0 = fsk_burst_detector(
            avg_len=100,
            cons_offset=3,
            decim=decim,
            fsk_dev=fsk_dev,
            interp=interp,
            samp_rate=samp_rate,
        )
        self.fhss_utils_tagged_burst_to_pdu_0 = fhss_utils.tagged_burst_to_pdu(1, decim_taps, min_burst_time, max_burst_time, 0.0, 1.0, 1.0, chan_samp_rate, 3)
        self.fhss_utils_fft_burst_tagger_0 = fhss_utils.fft_burst_tagger(rx_freq + chan_offset, fft_size, int(samp_rate / decim*interp / decim_2 * interp_2), int(round((float(chan_samp_rate)/fft_size)*pre_burst_time)), int(round((float(chan_samp_rate)/fft_size)*post_burst_time)), burst_width, 0, 0, trigger_thresh, int(round((float(samp_rate)/fft_size)*hist_time)), int(round((float(samp_rate)/fft_size)*lookahead_time)), True)
        self.fhss_utils_fft_burst_tagger_0.set_min_output_buffer(2048000)
        self.fhss_utils_cf_estimate_0 = fhss_utils.cf_estimate(fhss_utils.HALF_POWER, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate*rate_factor,True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, '', "")
        self.blocks_tag_debug_0.set_display(True)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 1)
        self.blocks_burst_tagger_0 = blocks.burst_tagger(gr.sizeof_gr_complex)
        self.blocks_burst_tagger_0.set_true_tag('burst_start',True)
        self.blocks_burst_tagger_0.set_false_tag('burst_stop',False)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_c(samp_rate *interp /decim, analog.GR_COS_WAVE, -1 * fine_offset, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -1 * chan_offset, 1, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, trigger_thresh)
        self.analog_agc2_xx_0 = analog.agc2_cc(10, 1e-1, 65536 / 10, 1)
        self.analog_agc2_xx_0.set_max_gain(65536 / 10)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.fhss_utils_cf_estimate_0, 'out'), (self.pdu_utils_pdu_fine_time_measure_0, 'pdu_in'))
        self.msg_connect((self.fhss_utils_tagged_burst_to_pdu_0, 'cpdus'), (self.fhss_utils_cf_estimate_0, 'in'))
        self.msg_connect((self.fhss_utils_tagged_burst_to_pdu_0, 'cpdus'), (self.pdu_utils_pdu_split_0, 'pdu_in'))
        self.msg_connect((self.pdu_utils_pdu_fine_time_measure_0, 'pdu_out'), (self.qtgui_waterfall_sink_x_0_1, 'in'))
        self.msg_connect((self.pdu_utils_pdu_split_0, 'dict'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.analog_agc2_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.blocks_burst_tagger_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_burst_tagger_0, 1))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.rational_resampler_xxx_1_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.fhss_utils_fft_burst_tagger_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.fhss_utils_fft_burst_tagger_0, 0), (self.fhss_utils_tagged_burst_to_pdu_0, 0))
        self.connect((self.fsk_burst_detector_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.fsk_burst_detector_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_freq_sink_x_1_0_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.blocks_burst_tagger_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.fhss_utils_fft_burst_tagger_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.fsk_burst_detector_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.qtgui_freq_sink_x_1_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))
        self.connect((self.sigmf_source_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "burst_rx_gmsk9600_ax25_playback")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_burst_width(self):
        return self.burst_width

    def set_burst_width(self, burst_width):
        self.burst_width = burst_width

    def get_chan_cutoff(self):
        return self.chan_cutoff

    def set_chan_cutoff(self, chan_cutoff):
        self.chan_cutoff = chan_cutoff
        self.set_decim_taps(firdes.low_pass(1.0, self.chan_samp_rate, self.chan_cutoff, self.chan_trans_width, firdes.WIN_HAMMING, 6.76))

    def get_chan_trans_width(self):
        return self.chan_trans_width

    def set_chan_trans_width(self, chan_trans_width):
        self.chan_trans_width = chan_trans_width
        self.set_decim_taps(firdes.low_pass(1.0, self.chan_samp_rate, self.chan_cutoff, self.chan_trans_width, firdes.WIN_HAMMING, 6.76))

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

    def get_hist_time(self):
        return self.hist_time

    def set_hist_time(self, hist_time):
        self.hist_time = hist_time

    def get_lookahead_time(self):
        return self.lookahead_time

    def set_lookahead_time(self, lookahead_time):
        self.lookahead_time = lookahead_time

    def get_max_burst_time(self):
        return self.max_burst_time

    def set_max_burst_time(self, max_burst_time):
        self.max_burst_time = max_burst_time

    def get_min_burst_time(self):
        return self.min_burst_time

    def set_min_burst_time(self, min_burst_time):
        self.min_burst_time = min_burst_time

    def get_post_burst_time(self):
        return self.post_burst_time

    def set_post_burst_time(self, post_burst_time):
        self.post_burst_time = post_burst_time

    def get_pre_burst_time(self):
        return self.pre_burst_time

    def set_pre_burst_time(self, pre_burst_time):
        self.pre_burst_time = pre_burst_time

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_chan_samp_rate(int(self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2))
        self.set_decim(int(self.samp_rate/2000))
        self.set_rx_offset(self.samp_rate/2.0)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate *self.interp /self.decim)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*self.rate_factor)
        self.fsk_burst_detector_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate / self.decim *self.interp, self.chan_filt_cutoff, self.chan_filt_trans, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)
        self.qtgui_freq_sink_x_1_0_1.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)

    def get_ts_str(self):
        return self.ts_str

    def set_ts_str(self, ts_str):
        self.ts_str = ts_str
        self.set_fn("VCC_{:s}_{:s}".format(self.gs_id, self.ts_str))

    def get_interp_2(self):
        return self.interp_2

    def set_interp_2(self, interp_2):
        self.interp_2 = interp_2
        self.set_chan_samp_rate(int(self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2))
        self.qtgui_freq_sink_x_1_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp
        self.set_chan_samp_rate(int(self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2))
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate *self.interp /self.decim)
        self.fsk_burst_detector_0.set_interp(self.interp)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate / self.decim *self.interp, self.chan_filt_cutoff, self.chan_filt_trans, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)

    def get_gs_id(self):
        return self.gs_id

    def set_gs_id(self, gs_id):
        self.gs_id = gs_id
        self.set_fn("VCC_{:s}_{:s}".format(self.gs_id, self.ts_str))

    def get_decim_2(self):
        return self.decim_2

    def set_decim_2(self, decim_2):
        self.decim_2 = decim_2
        self.set_chan_samp_rate(int(self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2))
        self.qtgui_freq_sink_x_1_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_chan_samp_rate(int(self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2))
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate *self.interp /self.decim)
        self.fsk_burst_detector_0.set_decim(self.decim)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate / self.decim *self.interp, self.chan_filt_cutoff, self.chan_filt_trans, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.samp_rate / self.decim*self.interp / self.decim_2 * self.interp_2)

    def get_fn(self):
        return self.fn

    def set_fn(self, fn):
        self.fn = fn
        self.set_fp("/vtgs/captures/vcc/{:s}".format(self.fn))

    def get_chan_samp_rate(self):
        return self.chan_samp_rate

    def set_chan_samp_rate(self, chan_samp_rate):
        self.chan_samp_rate = chan_samp_rate
        self.set_decim_taps(firdes.low_pass(1.0, self.chan_samp_rate, self.chan_cutoff, self.chan_trans_width, firdes.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_1.set_samp_rate(self.chan_samp_rate)
        self.qtgui_waterfall_sink_x_0_1.set_frequency_range(0, self.chan_samp_rate)

    def get_trigger_thresh(self):
        return self.trigger_thresh

    def set_trigger_thresh(self, trigger_thresh):
        self.trigger_thresh = trigger_thresh
        Qt.QMetaObject.invokeMethod(self._trigger_thresh_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.trigger_thresh)))
        self.analog_const_source_x_0.set_offset(self.trigger_thresh)

    def get_rx_offset(self):
        return self.rx_offset

    def set_rx_offset(self, rx_offset):
        self.rx_offset = rx_offset

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        Qt.QMetaObject.invokeMethod(self._rx_gain_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_gain)))

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        Qt.QMetaObject.invokeMethod(self._rx_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_freq)))
        self.qtgui_freq_sink_x_1_0_1.set_frequency_range(self.rx_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate)

    def get_rate_factor(self):
        return self.rate_factor

    def set_rate_factor(self, rate_factor):
        self.rate_factor = rate_factor
        Qt.QMetaObject.invokeMethod(self._rate_factor_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rate_factor)))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*self.rate_factor)

    def get_fsk_dev(self):
        return self.fsk_dev

    def set_fsk_dev(self, fsk_dev):
        self.fsk_dev = fsk_dev
        self.fsk_burst_detector_0.set_fsk_dev(self.fsk_dev)

    def get_fp(self):
        return self.fp

    def set_fp(self, fp):
        self.fp = fp

    def get_fine_offset(self):
        return self.fine_offset

    def set_fine_offset(self, fine_offset):
        self.fine_offset = fine_offset
        Qt.QMetaObject.invokeMethod(self._fine_offset_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.fine_offset)))
        self.analog_sig_source_x_0_0_0.set_frequency(-1 * self.fine_offset)

    def get_decim_taps(self):
        return self.decim_taps

    def set_decim_taps(self, decim_taps):
        self.decim_taps = decim_taps

    def get_chan_offset(self):
        return self.chan_offset

    def set_chan_offset(self, chan_offset):
        self.chan_offset = chan_offset
        Qt.QMetaObject.invokeMethod(self._chan_offset_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.chan_offset)))
        self.analog_sig_source_x_0_0.set_frequency(-1 * self.chan_offset)

    def get_chan_filt_trans(self):
        return self.chan_filt_trans

    def set_chan_filt_trans(self, chan_filt_trans):
        self.chan_filt_trans = chan_filt_trans
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate / self.decim *self.interp, self.chan_filt_cutoff, self.chan_filt_trans, firdes.WIN_HAMMING, 6.76))

    def get_chan_filt_cutoff(self):
        return self.chan_filt_cutoff

    def set_chan_filt_cutoff(self, chan_filt_cutoff):
        self.chan_filt_cutoff = chan_filt_cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate / self.decim *self.interp, self.chan_filt_cutoff, self.chan_filt_trans, firdes.WIN_HAMMING, 6.76))




def argument_parser():
    description = 'VCC Burst TX/RX, 9600 Baud GMSK, AX.25'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--burst-width", dest="burst_width", type=intx, default=int(20e3),
        help="Set Burst Width [Hz] [default=%(default)r]")
    parser.add_argument(
        "--chan-cutoff", dest="chan_cutoff", type=eng_float, default="12.0k",
        help="Set Channel Cutoff [default=%(default)r]")
    parser.add_argument(
        "--chan-trans-width", dest="chan_trans_width", type=eng_float, default="1.0k",
        help="Set Channel Trans. Width [cycles/samp] [default=%(default)r]")
    parser.add_argument(
        "--fft-size", dest="fft_size", type=intx, default=int(512),
        help="Set FFT Size [default=%(default)r]")
    parser.add_argument(
        "--hist-time", dest="hist_time", type=eng_float, default="75.0m",
        help="Set History Time [s] [default=%(default)r]")
    parser.add_argument(
        "--lookahead-time", dest="lookahead_time", type=eng_float, default="10.0m",
        help="Set Lookahead Time [s] [default=%(default)r]")
    parser.add_argument(
        "--max-burst-time", dest="max_burst_time", type=eng_float, default="250.0m",
        help="Set Max Burst Time [s] [default=%(default)r]")
    parser.add_argument(
        "--min-burst-time", dest="min_burst_time", type=eng_float, default="10.0m",
        help="Set Min Burst Time [s] [default=%(default)r]")
    parser.add_argument(
        "--post-burst-time", dest="post_burst_time", type=eng_float, default="500.0m",
        help="Set Post Burst Time [s] [default=%(default)r]")
    parser.add_argument(
        "--pre-burst-time", dest="pre_burst_time", type=eng_float, default="75.0m",
        help="Set Pre Burst Time [s] [default=%(default)r]")
    return parser


def main(top_block_cls=burst_rx_gmsk9600_ax25_playback, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(burst_width=options.burst_width, chan_cutoff=options.chan_cutoff, chan_trans_width=options.chan_trans_width, fft_size=options.fft_size, hist_time=options.hist_time, lookahead_time=options.lookahead_time, max_burst_time=options.max_burst_time, min_burst_time=options.min_burst_time, post_burst_time=options.post_burst_time, pre_burst_time=options.pre_burst_time)

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
