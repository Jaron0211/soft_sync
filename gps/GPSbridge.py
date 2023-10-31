#Hardware driver for UART GPS
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

        self.gps_time = 0
        self.status = ""
        self.latitude = 0
        self.latitude_hemisphere = 0
        self.longitude = 0
        self.longitude_hemisphere = 0
        self.speed = 0
        self.course = 0
        self.date = 0

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
                self.NMEA_GPRMC(self.GPS_data)
                self.find_header = False
                self._buff_msg = ''
                self.trigger = True
                self.freq = 1/(time.time() - self.frequence_timer + 0.00001)
                self.frequence_timer = time.time()
    
    def NMEA_GPRMC(self, msg):
        if len(msg) < 12 or msg[0] != "$GPRMC":
            self.gps_time = 0
            self.status = ""
            self.latitude = 0
            self.latitude_hemisphere = 0
            self.longitude = 0
            self.longitude_hemisphere = 0
            self.speed = 0
            self.course = 0
            self.date = 0
            return

        # Extract relevant fields
        time = msg[1]
        status = str(msg[2])
        latitude = msg[3]
        latitude_hemisphere = msg[4]
        longitude = msg[5]
        longitude_hemisphere = msg[6]
        speed = msg[7]
        course = msg[8]
        date = msg[9]

        # Check if the GPS fix is valid
        if status != "A":
            return None

        # Convert latitude and longitude from NMEA format to decimal degrees
        latitude_degrees = float(latitude[:2]) + float(latitude[2:]) / 60
        if latitude_hemisphere == "S":
            latitude_degrees = -latitude_degrees

        longitude_degrees = float(longitude[:3]) + float(longitude[3:]) / 60
        if longitude_hemisphere == "W":
            longitude_degrees = -longitude_degrees

        self.gps_time = msg[1]
        self.status = msg[2]
        self.latitude = latitude_degrees
        self.latitude_hemisphere = msg[4]
        self.longitude = longitude_degrees
        self.longitude_hemisphere = msg[6]
        self.speed = msg[7]
        self.course = msg[8]
        self.date = msg[9]


       
if __name__ == "__main__":
    GPS = _GPS_unit('COM6')

    while 1:
        GPS.run()
        if GPS.trigger:
            print(GPS.freq)
            print(GPS.GPS_data)

