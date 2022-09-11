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
import sip
from gnuradio import fosphor
from gnuradio.fft import window
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time

from gnuradio import qtgui

class uhd_iridium_rx_1(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "uhd_iridium_rx_1")

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
        self.samp_rate = samp_rate = 12.5e6
        self.decim = decim = 25
        self.rx_gain = rx_gain = 20
        self.ring_alert_label = ring_alert_label = "Ring Alert"
        self.iridium_rx_1_addr = iridium_rx_1_addr = "addr=10.51.2.10"
        self.full_band_label = full_band_label = "Full Band"
        self.fc_iridium = fc_iridium = 1621.25e6
        self.f_ring_alert = f_ring_alert = 1626.270833e6
        self.bpf_taps_cc = bpf_taps_cc = firdes.complex_band_pass(1.0, samp_rate, -samp_rate/2/decim, samp_rate/2/decim, 500e3, firdes.WIN_HAMMING, 6.76)
        self.bb_gain = bb_gain = 20

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
        self._bb_gain_tool_bar = Qt.QToolBar(self)
        self._bb_gain_tool_bar.addWidget(Qt.QLabel('bb_gain' + ": "))
        self._bb_gain_line_edit = Qt.QLineEdit(str(self.bb_gain))
        self._bb_gain_tool_bar.addWidget(self._bb_gain_line_edit)
        self._bb_gain_line_edit.returnPressed.connect(
            lambda: self.set_bb_gain(eng_notation.str_to_num(str(self._bb_gain_line_edit.text()))))
        self.top_grid_layout.addWidget(self._bb_gain_tool_bar, 4, 4, 1, 4)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join((iridium_rx_1_addr, "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(fc_iridium, samp_rate/2), 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self._ring_alert_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._ring_alert_label_formatter = None
        else:
            self._ring_alert_label_formatter = lambda x: str(x)

        self._ring_alert_label_tool_bar.addWidget(Qt.QLabel("Iridium" + ": "))
        self._ring_alert_label_label = Qt.QLabel(str(self._ring_alert_label_formatter(self.ring_alert_label)))
        self._ring_alert_label_tool_bar.addWidget(self._ring_alert_label_label)
        self.top_grid_layout.addWidget(self._ring_alert_label_tool_bar, 0, 4, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._full_band_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._full_band_label_formatter = None
        else:
            self._full_band_label_formatter = lambda x: str(x)

        self._full_band_label_tool_bar.addWidget(Qt.QLabel("Iridium" + ": "))
        self._full_band_label_label = Qt.QLabel(str(self._full_band_label_formatter(self.full_band_label)))
        self._full_band_label_tool_bar.addWidget(self._full_band_label_label)
        self.top_grid_layout.addWidget(self._full_band_label_tool_bar, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(25, bpf_taps_cc, f_ring_alert-fc_iridium, samp_rate)
        self.fosphor_qt_sink_c_0_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(0, samp_rate / decim)
        self._fosphor_qt_sink_c_0_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._fosphor_qt_sink_c_0_0_win, 1, 4, 3, 4)
        for r in range(1, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(0, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._fosphor_qt_sink_c_0_win, 1, 0, 3, 4)
        for r in range(1, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(bb_gain)
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, 1e-2, 0.1, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.fosphor_qt_sink_c_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.fosphor_qt_sink_c_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "uhd_iridium_rx_1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bpf_taps_cc(firdes.complex_band_pass(1.0, self.samp_rate, -self.samp_rate/2/self.decim, self.samp_rate/2/self.decim, 500e3, firdes.WIN_HAMMING, 6.76))
        self.fosphor_qt_sink_c_0.set_frequency_range(0, self.samp_rate)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(0, self.samp_rate / self.decim)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.fc_iridium, self.samp_rate/2), 0)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_bpf_taps_cc(firdes.complex_band_pass(1.0, self.samp_rate, -self.samp_rate/2/self.decim, self.samp_rate/2/self.decim, 500e3, firdes.WIN_HAMMING, 6.76))
        self.fosphor_qt_sink_c_0_0.set_frequency_range(0, self.samp_rate / self.decim)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        Qt.QMetaObject.invokeMethod(self._rx_gain_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_gain)))
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_ring_alert_label(self):
        return self.ring_alert_label

    def set_ring_alert_label(self, ring_alert_label):
        self.ring_alert_label = ring_alert_label
        Qt.QMetaObject.invokeMethod(self._ring_alert_label_label, "setText", Qt.Q_ARG("QString", self.ring_alert_label))

    def get_iridium_rx_1_addr(self):
        return self.iridium_rx_1_addr

    def set_iridium_rx_1_addr(self, iridium_rx_1_addr):
        self.iridium_rx_1_addr = iridium_rx_1_addr

    def get_full_band_label(self):
        return self.full_band_label

    def set_full_band_label(self, full_band_label):
        self.full_band_label = full_band_label
        Qt.QMetaObject.invokeMethod(self._full_band_label_label, "setText", Qt.Q_ARG("QString", self.full_band_label))

    def get_fc_iridium(self):
        return self.fc_iridium

    def set_fc_iridium(self, fc_iridium):
        self.fc_iridium = fc_iridium
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.f_ring_alert-self.fc_iridium)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.fc_iridium, self.samp_rate/2), 0)

    def get_f_ring_alert(self):
        return self.f_ring_alert

    def set_f_ring_alert(self, f_ring_alert):
        self.f_ring_alert = f_ring_alert
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.f_ring_alert-self.fc_iridium)

    def get_bpf_taps_cc(self):
        return self.bpf_taps_cc

    def set_bpf_taps_cc(self, bpf_taps_cc):
        self.bpf_taps_cc = bpf_taps_cc
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.bpf_taps_cc)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        Qt.QMetaObject.invokeMethod(self._bb_gain_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.bb_gain)))
        self.blocks_multiply_const_vxx_0.set_k(self.bb_gain)





def main(top_block_cls=uhd_iridium_rx_1, options=None):

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
