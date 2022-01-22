#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: wwv_dual_record_sigmf
# Author: Zach Leffke
# Description: Generic SigMF Recorder,
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
from datetime import datetime as dt; import string; import math
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time
import gr_sigmf
import timing_utils
import pmt

from gnuradio import qtgui

class wwv_dual_record_sigmf(gr.top_block, Qt.QWidget):

    def __init__(self, ant_pol_x='N-S', ant_pol_y='E-W', ant_type='KJ4QLP Active HF Dipole Balun', db_type='LFRX', decim=5, geo_alt=655.0, geo_lat=37.206756, geo_lon=-80.418876, interp=1, path="/captures/wwv", samp_rate=250e3, signal_type='WWV', usrp_addr="addr=10.41.1.11", usrp_clock_source="External", usrp_subdev_spec='A:A A:B', usrp_sync="Unknown PPS", usrp_time_source="External", usrp_type='N210'):
        gr.top_block.__init__(self, "wwv_dual_record_sigmf")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("wwv_dual_record_sigmf")
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

        self.settings = Qt.QSettings("GNU Radio", "wwv_dual_record_sigmf")

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
        self.ant_pol_x = ant_pol_x
        self.ant_pol_y = ant_pol_y
        self.ant_type = ant_type
        self.db_type = db_type
        self.decim = decim
        self.geo_alt = geo_alt
        self.geo_lat = geo_lat
        self.geo_lon = geo_lon
        self.interp = interp
        self.path = path
        self.samp_rate = samp_rate
        self.signal_type = signal_type
        self.usrp_addr = usrp_addr
        self.usrp_clock_source = usrp_clock_source
        self.usrp_subdev_spec = usrp_subdev_spec
        self.usrp_sync = usrp_sync
        self.usrp_time_source = usrp_time_source
        self.usrp_type = usrp_type

        ##################################################
        # Variables
        ##################################################
        self.ts_str = ts_str = dt.strftime(dt.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        self.fn_y = fn_y = "{:s}_{:s}_{:s}".format(signal_type.upper(), ant_pol_y, ts_str)
        self.fn_x = fn_x = "{:s}_{:s}_{:s}".format(signal_type.upper(), ant_pol_x, ts_str)
        self.variable_qtgui_label_1 = variable_qtgui_label_1 = "East/West"
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = "North/South"
        self.rx_freq = rx_freq = 10e6
        self.resamp_rate = resamp_rate = float(interp / decim * samp_rate)
        self.fp_y = fp_y = "{:s}/{:s}".format(path, fn_y)
        self.fp_x = fp_x = "{:s}/{:s}".format(path, fn_x)

        ##################################################
        # Blocks
        ##################################################
        self._rx_freq_tool_bar = Qt.QToolBar(self)
        self._rx_freq_tool_bar.addWidget(Qt.QLabel('rx_freq' + ": "))
        self._rx_freq_line_edit = Qt.QLineEdit(str(self.rx_freq))
        self._rx_freq_tool_bar.addWidget(self._rx_freq_line_edit)
        self._rx_freq_line_edit.returnPressed.connect(
            lambda: self.set_rx_freq(eng_notation.str_to_num(str(self._rx_freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._rx_freq_tool_bar, 0, 2, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_label_1_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_1_formatter = None
        else:
            self._variable_qtgui_label_1_formatter = lambda x: str(x)

        self._variable_qtgui_label_1_tool_bar.addWidget(Qt.QLabel('Antenna' + ": "))
        self._variable_qtgui_label_1_label = Qt.QLabel(str(self._variable_qtgui_label_1_formatter(self.variable_qtgui_label_1)))
        self._variable_qtgui_label_1_tool_bar.addWidget(self._variable_qtgui_label_1_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_1_tool_bar, 0, 4, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_formatter = None
        else:
            self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Antenna' + ": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join((usrp_addr, "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source_0.set_subdev_spec(usrp_subdev_spec, 0)
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(rx_freq, samp_rate/2), 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(rx_freq, samp_rate/2), 1)
        self.uhd_usrp_source_0.set_gain(0, 1)
        self.uhd_usrp_source_0.set_antenna('RX2', 1)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.timing_utils_usrp_gps_time_sync_0 = timing_utils.usrp_gps_time_sync(self,'uhd_usrp_source_0')
        self.timing_utils_system_time_tagger_0_0 = timing_utils.system_time_tagger_c(int(resamp_rate))
        self.timing_utils_system_time_tagger_0 = timing_utils.system_time_tagger_c(int(resamp_rate))
        self.timing_utils_system_time_diff_0_0 = timing_utils.system_time_diff_c(False,True)
        self.timing_utils_system_time_diff_0 = timing_utils.system_time_diff_c(False,True)
        self.sigmf_sink_1_0 = gr_sigmf.sink("cf32", fp_y, gr_sigmf.sigmf_time_mode_absolute, False)
        self.sigmf_sink_1_0.set_global_meta("core:sample_rate", resamp_rate)
        self.sigmf_sink_1_0.set_global_meta("core:description", 'WWV Dual Polarization Recorder')
        self.sigmf_sink_1_0.set_global_meta("core:author", 'Zach Leffke, KJ4QLP')
        self.sigmf_sink_1_0.set_global_meta("core:license", 'MIT')
        self.sigmf_sink_1_0.set_global_meta("core:hw", 'N210, LFRX, KJ4QLP AHFDB Antenna')

        self.sigmf_sink_1_0.set_global_meta("uhd:usrp_type", usrp_type)

        self.sigmf_sink_1_0.set_global_meta("uhd:db_type", db_type)

        self.sigmf_sink_1_0.set_global_meta("uhd:addr", usrp_addr)

        self.sigmf_sink_1_0.set_global_meta("uhd:subdev_spec", usrp_subdev_spec)

        self.sigmf_sink_1_0.set_global_meta("uhd:sync", usrp_sync)

        self.sigmf_sink_1_0.set_global_meta("uhd:clock_source", usrp_clock_source)

        self.sigmf_sink_1_0.set_global_meta("uhd:time_source", usrp_time_source)

        self.sigmf_sink_1_0.set_global_meta("misc:signal_type", signal_type)

        self.sigmf_sink_1_0.set_global_meta("ant:type", ant_type)

        self.sigmf_sink_1_0.set_global_meta("ant:pol", ant_pol_y)

        self.sigmf_sink_1_0.set_global_meta("geo:lat", "{:2.7f}".format(geo_lat))

        self.sigmf_sink_1_0.set_global_meta("geo:lon", "{:2.7f}".format(geo_lon))

        self.sigmf_sink_1_0.set_global_meta("geo:alt", "{:4.3f}".format(geo_alt))

        self.sigmf_sink_1_0.set_global_meta("misc:interpolation", interp)

        self.sigmf_sink_1_0.set_global_meta("misc:decimation", decim)
        self.sigmf_sink_1 = gr_sigmf.sink("cf32", fp_x, gr_sigmf.sigmf_time_mode_absolute, False)
        self.sigmf_sink_1.set_global_meta("core:sample_rate", resamp_rate)
        self.sigmf_sink_1.set_global_meta("core:description", 'WWV Dual Polarization Recorder')
        self.sigmf_sink_1.set_global_meta("core:author", 'Zach Leffke, KJ4QLP')
        self.sigmf_sink_1.set_global_meta("core:license", 'MIT')
        self.sigmf_sink_1.set_global_meta("core:hw", 'N210, LFRX, KJ4QLP AHFDB Antenna')

        self.sigmf_sink_1.set_global_meta("uhd:usrp_type", usrp_type)

        self.sigmf_sink_1.set_global_meta("uhd:db_type", db_type)

        self.sigmf_sink_1.set_global_meta("uhd:addr", usrp_addr)

        self.sigmf_sink_1.set_global_meta("uhd:subdev_spec", usrp_subdev_spec)

        self.sigmf_sink_1.set_global_meta("uhd:sync", usrp_sync)

        self.sigmf_sink_1.set_global_meta("uhd:clock_source", usrp_clock_source)

        self.sigmf_sink_1.set_global_meta("uhd:time_source", usrp_time_source)

        self.sigmf_sink_1.set_global_meta("misc:signal_type", signal_type)

        self.sigmf_sink_1.set_global_meta("ant:type", ant_type)

        self.sigmf_sink_1.set_global_meta("ant:pol", ant_pol_x)

        self.sigmf_sink_1.set_global_meta("geo:lat", "{:2.7f}".format(geo_lat))

        self.sigmf_sink_1.set_global_meta("geo:lon", "{:2.7f}".format(geo_lon))

        self.sigmf_sink_1.set_global_meta("geo:alt", "{:4.3f}".format(geo_alt))

        self.sigmf_sink_1.set_global_meta("misc:interpolation", interp)

        self.sigmf_sink_1.set_global_meta("misc:decimation", decim)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=interp,
                decimation=decim,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=interp,
                decimation=decim,
                taps=None,
                fractional_bw=None)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            resamp_rate, #bw
            "E-W", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.0050)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)



        labels = ['E-W', '', '', '', '',
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

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, -40)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_win, 7, 4, 2, 4)
        for r in range(7, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            resamp_rate, #bw
            "N-S", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.0050)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['N-S', '', '', '', '',
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

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, -40)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 5, 4, 2, 4)
        for r in range(5, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate / decim, #samp_rate
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 7, 0, 2, 4)
        for r in range(7, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            2
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(2):
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
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            resamp_rate, #bw
            "", #name
            2
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.0050)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, -40)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ["N-S", "E-W", '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 5, 0, 2, 4)
        for r in range(5, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fosphor_qt_sink_c_0_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_0.set_fft_window(window.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(0, samp_rate)
        self._fosphor_qt_sink_c_0_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._fosphor_qt_sink_c_0_0_win, 1, 4, 4, 4)
        for r in range(1, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(window.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(0, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._fosphor_qt_sink_c_0_win, 1, 0, 4, 4)
        for r in range(1, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, '', "")
        self.blocks_tag_debug_0.set_display(True)
        self.blocks_socket_pdu_0 = blocks.socket_pdu('TCP_SERVER', '0.0.0.0', '52001', 10000, False)
        self.blocks_message_debug_0 = blocks.message_debug()


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.fosphor_qt_sink_c_0_0, 'freq'), (self.timing_utils_usrp_gps_time_sync_0, 'in'))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.timing_utils_system_time_tagger_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.timing_utils_system_time_tagger_0, 0))
        self.connect((self.timing_utils_system_time_diff_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.timing_utils_system_time_diff_0, 1), (self.qtgui_number_sink_0, 0))
        self.connect((self.timing_utils_system_time_diff_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.timing_utils_system_time_diff_0, 0), (self.sigmf_sink_1, 0))
        self.connect((self.timing_utils_system_time_diff_0_0, 0), (self.blocks_tag_debug_0, 1))
        self.connect((self.timing_utils_system_time_diff_0_0, 1), (self.qtgui_number_sink_0, 1))
        self.connect((self.timing_utils_system_time_diff_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.timing_utils_system_time_diff_0_0, 0), (self.sigmf_sink_1_0, 0))
        self.connect((self.timing_utils_system_time_tagger_0, 0), (self.timing_utils_system_time_diff_0_0, 0))
        self.connect((self.timing_utils_system_time_tagger_0_0, 0), (self.timing_utils_system_time_diff_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.fosphor_qt_sink_c_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.fosphor_qt_sink_c_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.rational_resampler_xxx_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "wwv_dual_record_sigmf")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_ant_pol_x(self):
        return self.ant_pol_x

    def set_ant_pol_x(self, ant_pol_x):
        self.ant_pol_x = ant_pol_x
        self.set_fn_x("{:s}_{:s}_{:s}".format(signal_type.upper(), self.ant_pol_x, self.ts_str))

    def get_ant_pol_y(self):
        return self.ant_pol_y

    def set_ant_pol_y(self, ant_pol_y):
        self.ant_pol_y = ant_pol_y
        self.set_fn_y("{:s}_{:s}_{:s}".format(signal_type.upper(), self.ant_pol_y, self.ts_str))

    def get_ant_type(self):
        return self.ant_type

    def set_ant_type(self, ant_type):
        self.ant_type = ant_type

    def get_db_type(self):
        return self.db_type

    def set_db_type(self, db_type):
        self.db_type = db_type

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_resamp_rate(float(self.interp / self.decim * self.samp_rate))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate / self.decim)

    def get_geo_alt(self):
        return self.geo_alt

    def set_geo_alt(self, geo_alt):
        self.geo_alt = geo_alt

    def get_geo_lat(self):
        return self.geo_lat

    def set_geo_lat(self, geo_lat):
        self.geo_lat = geo_lat

    def get_geo_lon(self):
        return self.geo_lon

    def set_geo_lon(self, geo_lon):
        self.geo_lon = geo_lon

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp
        self.set_resamp_rate(float(self.interp / self.decim * self.samp_rate))

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path
        self.set_fp_x("{:s}/{:s}".format(self.path, self.fn_x))
        self.set_fp_y("{:s}/{:s}".format(self.path, self.fn_y))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_resamp_rate(float(self.interp / self.decim * self.samp_rate))
        self.fosphor_qt_sink_c_0.set_frequency_range(0, self.samp_rate)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate / self.decim)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/2), 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/2), 1)

    def get_signal_type(self):
        return self.signal_type

    def set_signal_type(self, signal_type):
        self.signal_type = signal_type

    def get_usrp_addr(self):
        return self.usrp_addr

    def set_usrp_addr(self, usrp_addr):
        self.usrp_addr = usrp_addr

    def get_usrp_clock_source(self):
        return self.usrp_clock_source

    def set_usrp_clock_source(self, usrp_clock_source):
        self.usrp_clock_source = usrp_clock_source

    def get_usrp_subdev_spec(self):
        return self.usrp_subdev_spec

    def set_usrp_subdev_spec(self, usrp_subdev_spec):
        self.usrp_subdev_spec = usrp_subdev_spec

    def get_usrp_sync(self):
        return self.usrp_sync

    def set_usrp_sync(self, usrp_sync):
        self.usrp_sync = usrp_sync

    def get_usrp_time_source(self):
        return self.usrp_time_source

    def set_usrp_time_source(self, usrp_time_source):
        self.usrp_time_source = usrp_time_source

    def get_usrp_type(self):
        return self.usrp_type

    def set_usrp_type(self, usrp_type):
        self.usrp_type = usrp_type

    def get_ts_str(self):
        return self.ts_str

    def set_ts_str(self, ts_str):
        self.ts_str = ts_str
        self.set_fn_x("{:s}_{:s}_{:s}".format(signal_type.upper(), self.ant_pol_x, self.ts_str))
        self.set_fn_y("{:s}_{:s}_{:s}".format(signal_type.upper(), self.ant_pol_y, self.ts_str))

    def get_fn_y(self):
        return self.fn_y

    def set_fn_y(self, fn_y):
        self.fn_y = fn_y
        self.set_fp_y("{:s}/{:s}".format(self.path, self.fn_y))

    def get_fn_x(self):
        return self.fn_x

    def set_fn_x(self, fn_x):
        self.fn_x = fn_x
        self.set_fp_x("{:s}/{:s}".format(self.path, self.fn_x))

    def get_variable_qtgui_label_1(self):
        return self.variable_qtgui_label_1

    def set_variable_qtgui_label_1(self, variable_qtgui_label_1):
        self.variable_qtgui_label_1 = variable_qtgui_label_1
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_1_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_1))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0))

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        Qt.QMetaObject.invokeMethod(self._rx_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_freq)))
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/2), 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.samp_rate/2), 1)

    def get_resamp_rate(self):
        return self.resamp_rate

    def set_resamp_rate(self, resamp_rate):
        self.resamp_rate = resamp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.resamp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.resamp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.resamp_rate)

    def get_fp_y(self):
        return self.fp_y

    def set_fp_y(self, fp_y):
        self.fp_y = fp_y

    def get_fp_x(self):
        return self.fp_x

    def set_fp_x(self, fp_x):
        self.fp_x = fp_x




def argument_parser():
    description = 'Generic SigMF Recorder,'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--ant-pol-x", dest="ant_pol_x", type=str, default='N-S',
        help="Set ant_pol_x [default=%(default)r]")
    parser.add_argument(
        "--ant-pol-y", dest="ant_pol_y", type=str, default='E-W',
        help="Set ant_pol_y [default=%(default)r]")
    parser.add_argument(
        "--ant-type", dest="ant_type", type=str, default='KJ4QLP Active HF Dipole Balun',
        help="Set ant_type [default=%(default)r]")
    parser.add_argument(
        "--db-type", dest="db_type", type=str, default='LFRX',
        help="Set db_type [default=%(default)r]")
    parser.add_argument(
        "--decim", dest="decim", type=intx, default=5,
        help="Set decim [default=%(default)r]")
    parser.add_argument(
        "--geo-alt", dest="geo_alt", type=eng_float, default="655.0",
        help="Set geo_alt [default=%(default)r]")
    parser.add_argument(
        "--geo-lat", dest="geo_lat", type=eng_float, default="37.2068",
        help="Set geo_lat [default=%(default)r]")
    parser.add_argument(
        "--geo-lon", dest="geo_lon", type=eng_float, default="-80.4189",
        help="Set geo_lon [default=%(default)r]")
    parser.add_argument(
        "--interp", dest="interp", type=intx, default=1,
        help="Set interp [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default="250.0k",
        help="Set samp_rate [default=%(default)r]")
    parser.add_argument(
        "--signal-type", dest="signal_type", type=str, default='WWV',
        help="Set signal_type [default=%(default)r]")
    parser.add_argument(
        "--usrp-addr", dest="usrp_addr", type=str, default="addr=10.41.1.11",
        help="Set usrp_addr [default=%(default)r]")
    parser.add_argument(
        "--usrp-clock-source", dest="usrp_clock_source", type=str, default="External",
        help="Set usrp_clock_source [default=%(default)r]")
    parser.add_argument(
        "--usrp-subdev-spec", dest="usrp_subdev_spec", type=str, default='A:A A:B',
        help="Set usrp_subdev_spec [default=%(default)r]")
    parser.add_argument(
        "--usrp-sync", dest="usrp_sync", type=str, default="Unknown PPS",
        help="Set usrp_sync [default=%(default)r]")
    parser.add_argument(
        "--usrp-time-source", dest="usrp_time_source", type=str, default="External",
        help="Set usrp_time_source [default=%(default)r]")
    parser.add_argument(
        "--usrp-type", dest="usrp_type", type=str, default='N210',
        help="Set usrp_type [default=%(default)r]")
    return parser


def main(top_block_cls=wwv_dual_record_sigmf, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(ant_pol_x=options.ant_pol_x, ant_pol_y=options.ant_pol_y, ant_type=options.ant_type, db_type=options.db_type, decim=options.decim, geo_alt=options.geo_alt, geo_lat=options.geo_lat, geo_lon=options.geo_lon, interp=options.interp, samp_rate=options.samp_rate, signal_type=options.signal_type, usrp_addr=options.usrp_addr, usrp_clock_source=options.usrp_clock_source, usrp_subdev_spec=options.usrp_subdev_spec, usrp_sync=options.usrp_sync, usrp_time_source=options.usrp_time_source, usrp_type=options.usrp_type)

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
