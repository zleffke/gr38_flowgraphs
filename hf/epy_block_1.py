#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018, 2019, 2020 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government
# retains certain rights in this software.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright 2022, Zach Leffke
# Modifying sandia's GPS Time Sync to use NTP time....not yet sure if its a good idea...

import numpy as np
from gnuradio import gr
import uhd
import time
import pmt
import inspect
import gc

class usrp_ntp_pps_sync(gr.sync_block):
    """
    Synchronize a USRP to NTP time
    To provide synchronziation across USRP devices, the radio time within the
    hardware will be set to the correct GPS epoch on a received PPS interval.
    To synchronize, a PPS is associated with a GPS epoch by monitoring the
    received GPS time and the last observed PPS time.  Once a known boundary
    is observed, on the next PPS, the radio time is set to the correct GPS
    epoch.
    If the GPSDO is not available or is unlocked, the time will be set to the
    current system time.   
    The time can be resynchronized by publishing a message into the block at  any time.  
    This DOES cause the USRP object to be stopped during the time synchronization.
    It is recommended to use a USRP source object for synchronization.
    
    Synchronize a USRP to PPS time using NTP
    NTP is used as a coarse time reference.
    PPS is used for fine time alignment.
    Goal is a
    """
    def __init__(self, parent="", usrp_id="uhd_usrp_source_0", verbose=False):
        gr.sync_block.__init__(self,
            name="usrp_ntp_pps_sync",
            in_sig=None,
            out_sig=None)
            
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.msg_handler)

        # setup logger
        logger_name = 'gr_log.' + self.to_basic_block().alias()
        if logger_name in gr.logger_get_names():
            self.log = gr.logger(logger_name)
        else:
            self.log = gr.logger('log')
        
        
        self.parent = inspect.currentframe().f_back
        #print(self.parent)
        print(inspect.getmembers(self.parent))
        self.usrp_id = usrp_id
        self.verbose = verbose

        self.usrp = None
        self.locked = False

      

    def start(self):
        self.log.debug("Starting GPS Time Sync")

        '''
        Overload start function
        '''
        try:
          # Check to ensure
            #self.usrp_source_object = eval("self.parent.%s"%self.usrp_source)
            self._get_usrp_object()
            print(self.usrp)
            return true

        #except AttributeError:
        #    self.log.error("Unable to acquire usrp object for synchronization")
        #    return True
        
        except Exception as e:
            self.log.error(repr(e))

        # synchronize
        self.synchronize()

        # if not locked, default time to current system time
        if not self.locked:
            try:
                self.log.debug("USRP GPS Time Sync: Defaulting to Current System Time")
                self.usrp.set_time_now(uhd.time_spec_t(time.time()))
            except Exception as e:
                self.log.error("Set Time Next PPS Error: " + repr(e))

        return True

    def _get_usrp_object(self):
        #my_usrp = uhd.usrp.MultiUSRP(self.usrp_id)
        #self.usrp = my_usrp
        self.parent = eval("self.%s"%self.parent)
        print(self.parent)
        self.usrp_source_object = eval("self.parent.%s"%self.usrp_source)
        print(self.usrp_source_object)
        return
        
    def _stop_usrp(self):
        # Stop Stream
        st_args = uhd.usrp.StreamArgs("fc32", "sc16")
        streamer = self.usrp.get_rx_stream(st_args)
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
        streamer.issue_stream_cmd(stream_cmd)
        self.log.debug("USRP Object Stopped for Time Synchronization")
    
    def _start_usrp(self):
        st_args = uhd.usrp.StreamArgs("fc32", "sc16")
        streamer = self.usrp.get_rx_stream(st_args)
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        streamer.issue_stream_cmd(stream_cmd)
        self.log.debug("USRP Objected Restarted After Time Synchronization")
        
    def synchronize(self):
        '''
        0. Stop USRP.
        1. Get USRP Sensors, mainly checking for PPS input. 
        2. Poll PPS for input.
        3. on PPS event, get current PC Time (aka Wall Clock, assumes locked with NTP)
           Assume the wall clock is hapening AFTER the PPS...expect milliseconds
        4. Round up Wall Clock time to the next second rollover, 0 fractional seconds
        5. On next PPS event, set USRP time.
        6. Some kind of time check.....maybe compare next PPS with current USRP time.
        7. return true/false...if not true set usrp time to current system time (with ntp level slop)
        8. restart USRP.
        '''
        
        # check usrp object, if none return and set time with NTP slop
        if (self.usrp == None):
            return False
            
        # 0. Stop USRP.
        self._stop_usrp()
        
        #1. Get USRP Sensors, mainly checking for PPS input. 
#        pps_seconds = self.usrp.get_time_last_pps().to_ticks(1.0)
#        self.log.debug("pps_seconds = " + repr(pps_seconds))

        #2. Poll PPS for input.
        #3. on PPS event, get current PC Time (aka Wall Clock, assumes locked with NTP)
        #   Assume the wall clock is hapening AFTER the PPS...expect milliseconds
        #4. Round up Wall Clock time to the next second rollover, 0 fractional seconds
        #5. On next PPS event, set USRP time.
        #6. Some kind of time check.....maybe compare next PPS with current USRP time.
        #7. return true/false...if not true set usrp time to current system time (with ntp level slop)
        
        #8. restart USRP.
        self._start_usrp()
        return       
        
    def get_unixtime(self):
        t_now = np.datetime64(datetime.datetime.utcnow())  #reads PC Clock
        
        

    def synchronize_old(self):
      if (self.usrp_source_object == None):
        return False

      # check if gps is locked
      locked = self.usrp_source_object.get_mboard_sensor("gps_locked").to_bool()

      # only set time if changing from unlocked to locked
      if (self.gps_locked) and (locked):
        # no change in lock status
        self.gps_locked = locked
        return True
      elif (self.gps_locked) and (not locked):
        # system became unlocked - do nothing
        self.gps_locked = locked
        return True
      elif (not self.gps_locked) and (not locked):
        # system remains unlocked
        self.gps_locked = locked
        return True
      else:
        # system has gone from unlocked to locked
        self.gps_locked = locked
        pass

      # stop first
      self.usrp_source_object.stop()
      self.log.debug("USRP Object Stopped for Time Synchronization")

      # TODO: Find way to ensure we poll as closely to the second boundary as
      # possible to ensure we get as accurate a reading as possible
        #gps_time = self.usrp_source_object.get_mboard_sensor("gps_time")

      ## check PPS and compare UHD device time to GPS time
      ## we only care about the full seconds for now
      #gps_time = self.usrp_source_object.get_mboard_sensor("gps_time")
      #print "gps_time = " + repr(gps_time)
      #last_pps_time = self.usrp_source_object.get_time_last_pps()
      #print "last_pps_time = " + repr(last_pps_time)

      # we only care about the full seconds
      gps_seconds = self.usrp_source_object.get_mboard_sensor("gps_time").to_int()
      self.log.debug("gps_seconds = " + repr(gps_seconds))
      pps_seconds = self.usrp_source_object.get_time_last_pps().to_ticks(1.0)
      self.log.debug("pps_seconds = " + repr(pps_seconds))

      if (pps_seconds != gps_seconds):
        self.log.debug("Trying to align the device time to GPS time...")
        try:
          self.usrp_source_object.set_time_next_pps(uhd.time_spec_t(gps_seconds + 1))
        except Exception as e:
          self.log.error("Set Time Next PPS Error: " + repr(e))

        # allow some time to make sure the PPS has come
        time.sleep(1.1)

        # check again
        gps_seconds = self.usrp_source_object.get_mboard_sensor("gps_time").to_int()
        self.log.debug("updated gps_time = " + repr(gps_seconds))
        pps_seconds = self.usrp_source_object.get_time_last_pps().to_ticks(1.0)
        self.log.debug("updated last_pps_time = " + repr(pps_seconds))

      if (pps_seconds == gps_seconds):
        self.log.debug("Successful USRP GPS Time Synchronization")
      else:
        self.log.debug("Unable to synchronize GPS time")

      # set start time in future
      self.usrp_source_object.set_start_time(uhd.time_spec_t(gps_seconds+2.0))

      # restart
      self.usrp_source_object.start()
      self.log.debug("USRP Objected Restarted After Time Synchronization")

      return True

    def msg_handler(self,p):
      self.synchronize()

    def work(self, input_items, output_items):
      pass
