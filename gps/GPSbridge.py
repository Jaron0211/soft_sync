from __future__ import print_function
import sys
import os

import serial
import numpy as np
import time
import ctypes

class _GPS_unit():
    def __init__(self,port,baudrate=115200):
        self.ser = serial.Serial(port,baudrate,parity=serial.PARITY_NONE, rtscts=1,timeout=0.001)
        if self.ser.is_open:
            self.ser.close()

        self.ser.open()
        self.ser.flush()
        self.GPS_data = []
        self.trigger = False

        self._buff_msg = ''
        self.find_header = False
        self.frequence_timer = time.time()
        self.freq = 0

    # def read_serial(self):

    #     _buff = self.ser.readlines()
    #     trigger = False
    #     if len(_buff) > 0:
    #         self.GPS_data = [x.decode("ASCII")[:-2] for x in _buff if b"GPTXT" not in x]
    #         trigger = True

    #     return trigger

    def run(self):

        _buff = self.ser.read()
        self.trigger = False

        if _buff == b'$' and not self.find_header:
            self.find_header = True

        elif self.find_header:
            if _buff != b'':
                if _buff != b'$':
                    self._buff_msg += _buff.decode('ASCII')
            else:
                self.GPS_data = self._buff_msg.split('\r\n')[:-1]
                self.find_header = False
                self._buff_msg = ''
                self.trigger = True
                self.freq = 1/(time.time() - self.frequence_timer + 0.00001)
                self.frequence_timer = time.time()


       
if __name__ == "__main__":
    GPS = _GPS_unit('COM6')

    while 1:
        GPS.run()
        if GPS.trigger:
            print(GPS.freq)
            print(GPS.GPS_data)

