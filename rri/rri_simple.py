#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Simple RRI Test
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
import sip
from gnuradio import fosphor
from gnuradio.fft import window
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx

from gnuradio import qtgui

class rri_simple(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Simple RRI Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Simple RRI Test")
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

        self.settings = Qt.QSettings("GNU Radio", "rri_simple")

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
        self.rri_samp_rate = rri_samp_rate = 62500.33933
        self.fr_ratio = fr_ratio = rri_samp_rate / 32e3
        self.throttle = throttle = 10
        self.samp_rate = samp_rate = rri_samp_rate / fr_ratio
        self.fc = fc = 4350023.613248409

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
        self.mmse_resampler_xx_0_0 = filter.mmse_resampler_cc(0, fr_ratio)
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, fr_ratio)
        self.fosphor_qt_sink_c_0_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(fc, samp_rate)
        self._fosphor_qt_sink_c_0_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._fosphor_qt_sink_c_0_0_win, 4, 4, 2, 4)
        for r in range(4, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(firdes.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(fc, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._fosphor_qt_sink_c_0_win, 4, 0, 2, 4)
        for r in range(4, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, rri_samp_rate*throttle,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, rri_samp_rate*throttle,True)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/zleffke/github/zleffke/python/python_scripts/rri/dipole1.dat', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/zleffke/github/zleffke/python/python_scripts/rri/dipole2.dat', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.mmse_resampler_xx_0_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.fosphor_qt_sink_c_0_0, 0))
        self.connect((self.mmse_resampler_xx_0_0, 0), (self.fosphor_qt_sink_c_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rri_simple")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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
        self.fosphor_qt_sink_c_0.set_frequency_range(self.fc, self.samp_rate)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(self.fc, self.samp_rate)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.fosphor_qt_sink_c_0.set_frequency_range(self.fc, self.samp_rate)
        self.fosphor_qt_sink_c_0_0.set_frequency_range(self.fc, self.samp_rate)





def main(top_block_cls=rri_simple, options=None):

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
