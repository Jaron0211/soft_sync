from __future__ import print_function
import sys
import os

import serial
import numpy as np
import time
from dataclasses import dataclass

import pynmea2
#https://github.com/Knio/pynmea2

class _GPS_unit():
    def __init__(self,port,baudrate=115200):
        self.ser = serial.Serial(port,baudrate,parity=serial.PARITY_NONE, rtscts=1)
        if self.ser.is_open:
            self.ser.close()

        self.ser.open()

    def read_serial(self):
        _buff = self.ser.readline()
        
        return _buff
    
    
    
GPS = _GPS_unit('COM4')

while(1):
    gps_income = GPS.read_serial().decode("ASCII")
    msg = pynmea2.parse(gps_income[:-1])
    
    #print((msg.sentence_type))
    #print(GPS.read_serial().decode("ASCII")[:-1])
    #print("-------------------------")