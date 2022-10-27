from __future__ import print_function
import sys
import os

import serial
import numpy as np
import time
from dataclasses import dataclass

class _GPS_unit():
    def __init__(self,port,baudrate=115200):
        self.ser = serial.Serial(port,baudrate,parity=serial.PARITY_NONE, rtscts=1)
		if self.ser.is_open:
			self.ser.close()

		self.ser.open()