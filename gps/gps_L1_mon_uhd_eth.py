#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Iridium RX, N210, UBX-40
# Author: Zach Leffke, KJ4QLP
# Copyright: MIT
# Description: Iridium Full Band with Fosphor
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
from gnuradio import analog
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time

from gnuradio import qtgui

class gps_L1_mon_uhd_eth(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Iridium RX, N210, UBX-40")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Iridium RX, N210, UBX-40")
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

        self.settings = Qt.QSettings("GNU Radio", "gps_L1_mon_uhd_eth")

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
        self.samp_rate = samp_rate = 5e6
        self.fc_gps_l1 = fc_gps_l1 = 1575.42e6
        self.decim = decim = 125
        self.uhd_fc_tune = uhd_fc_tune = uhd.tune_request(fc_gps_l1, samp_rate/2)
        self.rx_gain = rx_gain = 45
        self.narrow_label = narrow_label = "L1 - Narrow"
        self.iridium_rx_1_addr = iridium_rx_1_addr = "addr=10.51.2.10"
        self.interp = interp = 1
        self.full_band_label = full_band_label = "L1 Full Band"
        self.fc_interferer = fc_interferer = -420e3
        self.bpf_taps_cc = bpf_taps_cc = firdes.complex_band_pass(1.0, samp_rate, -samp_rate/2/decim, samp_rate/2/decim, 500e3, firdes.WIN_HAMMING, 6.76)
        self.L1Hunt_addr = L1Hunt_addr = "addr=10.41.1.13"

        ##################################################
        # Blocks
        ##################################################
        self._rx_gain_tool_bar = Qt.QToolBar(self)
        self._rx_gain_tool_bar.addWidget(Qt.QLabel('rx_gain' + ": "))
        self._rx_gain_line_edit = Qt.QLineEdit(str(self.rx_gain))
        self._rx_gain_tool_bar.addWidget(self._rx_gain_line_edit)
        self._rx_gain_line_edit.returnPressed.connect(
            lambda: self.set_rx_gain(eng_notation.str_to_num(str(self._rx_gain_line_edit.text()))))
        self.top_grid_layout.addWidget(self._rx_gain_tool_bar, 4, 0, 1, 4)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._fc_interferer_tool_bar = Qt.QToolBar(self)
        self._fc_interferer_tool_bar.addWidget(Qt.QLabel('fc_interferer' + ": "))
        self._fc_interferer_line_edit = Qt.QLineEdit(str(self.fc_interferer))
        self._fc_interferer_tool_bar.addWidget(self._fc_interferer_line_edit)
        self._fc_interferer_line_edit.returnPressed.connect(
            lambda: self.set_fc_interferer(eng_notation.str_to_num(str(self._fc_interferer_line_edit.text()))))
        self.top_layout.addWidget(self._fc_interferer_tool_bar)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join((L1Hunt_addr, "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_center_freq(uhd_fc_tune, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=interp,
                decimation=1,
                taps=None,
                fractional_bw=None)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate/decim*interp, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.010)
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
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 2, 4, 2, 4)
        for r in range(2, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            4096, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            fc_gps_l1 + fc_interferer, #fc
            samp_rate / decim * interp, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.010)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        self.qtgui_freq_sink_x_0.disable_legend()


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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 4, 1, 4)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._narrow_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._narrow_label_formatter = None
        else:
            self._narrow_label_formatter = lambda x: str(x)

        self._narrow_label_tool_bar.addWidget(Qt.QLabel("GPS" + ": "))
        self._narrow_label_label = Qt.QLabel(str(self._narrow_label_formatter(self.narrow_label)))
        self._narrow_label_tool_bar.addWidget(self._narrow_label_label)
        self.top_grid_layout.addWidget(self._narrow_label_tool_bar, 0, 4, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._full_band_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._full_band_label_formatter = None
        else:
            self._full_band_label_formatter = lambda x: str(x)

        self._full_band_label_tool_bar.addWidget(Qt.QLabel("GPS" + ": "))
        self._full_band_label_label = Qt.QLabel(str(self._full_band_label_formatter(self.full_band_label)))
        self._full_band_label_tool_bar.addWidget(self._full_band_label_label)
        self.top_grid_layout.addWidget(self._full_band_label_tool_bar, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decim, bpf_taps_cc, fc_interferer, samp_rate)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(0, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._fosphor_qt_sink_c_0_win, 1, 0, 3, 4)
        for r in range(1, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, 1e-2, 0.1, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.fosphor_qt_sink_c_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_agc2_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gps_L1_mon_uhd_eth")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bpf_taps_cc(firdes.complex_band_pass(1.0, self.samp_rate, -self.samp_rate/2/self.decim, self.samp_rate/2/self.decim, 500e3, firdes.WIN_HAMMING, 6.76))
        self.set_uhd_fc_tune(uhd.tune_request(self.fc_gps_l1, self.samp_rate/2))
        self.fosphor_qt_sink_c_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc_gps_l1 + self.fc_interferer, self.samp_rate / self.decim * self.interp)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate/self.decim*self.interp)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_fc_gps_l1(self):
        return self.fc_gps_l1

    def set_fc_gps_l1(self, fc_gps_l1):
        self.fc_gps_l1 = fc_gps_l1
        self.set_uhd_fc_tune(uhd.tune_request(self.fc_gps_l1, self.samp_rate/2))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc_gps_l1 + self.fc_interferer, self.samp_rate / self.decim * self.interp)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_bpf_taps_cc(firdes.complex_band_pass(1.0, self.samp_rate, -self.samp_rate/2/self.decim, self.samp_rate/2/self.decim, 500e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc_gps_l1 + self.fc_interferer, self.samp_rate / self.decim * self.interp)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate/self.decim*self.interp)

    def get_uhd_fc_tune(self):
        return self.uhd_fc_tune

    def set_uhd_fc_tune(self, uhd_fc_tune):
        self.uhd_fc_tune = uhd_fc_tune
        self.uhd_usrp_source_0.set_center_freq(self.uhd_fc_tune, 0)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        Qt.QMetaObject.invokeMethod(self._rx_gain_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_gain)))
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_narrow_label(self):
        return self.narrow_label

    def set_narrow_label(self, narrow_label):
        self.narrow_label = narrow_label
        Qt.QMetaObject.invokeMethod(self._narrow_label_label, "setText", Qt.Q_ARG("QString", self.narrow_label))

    def get_iridium_rx_1_addr(self):
        return self.iridium_rx_1_addr

    def set_iridium_rx_1_addr(self, iridium_rx_1_addr):
        self.iridium_rx_1_addr = iridium_rx_1_addr

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc_gps_l1 + self.fc_interferer, self.samp_rate / self.decim * self.interp)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate/self.decim*self.interp)

    def get_full_band_label(self):
        return self.full_band_label

    def set_full_band_label(self, full_band_label):
        self.full_band_label = full_band_label
        Qt.QMetaObject.invokeMethod(self._full_band_label_label, "setText", Qt.Q_ARG("QString", self.full_band_label))

    def get_fc_interferer(self):
        return self.fc_interferer

    def set_fc_interferer(self, fc_interferer):
        self.fc_interferer = fc_interferer
        Qt.QMetaObject.invokeMethod(self._fc_interferer_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.fc_interferer)))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.fc_interferer)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc_gps_l1 + self.fc_interferer, self.samp_rate / self.decim * self.interp)

    def get_bpf_taps_cc(self):
        return self.bpf_taps_cc

    def set_bpf_taps_cc(self, bpf_taps_cc):
        self.bpf_taps_cc = bpf_taps_cc
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.bpf_taps_cc)

    def get_L1Hunt_addr(self):
        return self.L1Hunt_addr

    def set_L1Hunt_addr(self, L1Hunt_addr):
        self.L1Hunt_addr = L1Hunt_addr





def main(top_block_cls=gps_L1_mon_uhd_eth, options=None):

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
