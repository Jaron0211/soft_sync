from __future__ import print_function
import sys
import os

import serial
import numpy as np
import time
import ctypes

class _GPS_unit():
    def __init__(self,port,baudrate=115200):
        self.ser = serial.Serial(port,baudrate,parity=serial.PARITY_NONE, rtscts=1,timeout=0.01)
        if self.ser.is_open:
            self.ser.close()

        self.ser.open()
        self.GPS_data = []
        self.trigger = False

    def read_serial(self):

        _buff = self.ser.readlines()
        trigger = False
        if len(_buff) > 0:
            self.GPS_data = [x.decode("ASCII")[:-2] for x in _buff if b"GPTXT" not in x]
            trigger = True

        return trigger
            

    def run(self):
        self.trigger = self.read_serial()

       
if __name__ == "__main__":
    GPS = _GPS_unit('COM4')
    #GPS.start()
    while 1:
        GPS.run()
        if GPS.trigger:
            print(GPS.GPS_data)

