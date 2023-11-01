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

        #GPRMC
        self.UTC_hhmmss = 0
        self.status = ""
        self.latitude = 0
        self.latitude_hemisphere = 'N'
        self.longitude = 0
        self.longitude_hemisphere = 'E'
        #self.gs_mile = 0
        #self.TN_heading = 0
        self.UTC_ddmmyy = 0
        self.Mag_dec = 0
        self.Mag_dec_dir = 'E'
        self.date = 0
        self.mode_indicate = 'N'

        #GPVTG
        self.TN_heading = 0
        self.MN_heading = 0
        self.gs_mile = 0
        self.gs_km = 0
        #self.mode_indicate = 0

        #GPGGA
        #self.gps_time = 0
        #self.latitude = 0
        #self.latitude_hemisphere = 'N'
        #self.longitude = 0
        #self.longitude_hemisphere = 'E'
        self.GGA_mode_indicate = 0
        self.sat_num = 0
        self.HDOP = 99.9
        self.sea_alt = -9999.9
       


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
                self.NMEA(self.GPS_data)
                self.find_header = False
                self._buff_msg = ''
                self.trigger = True
                self.freq = 1/(time.time() - self.frequence_timer + 0.00001)
                self.frequence_timer = time.time()
    #Gps module output example
    '''
    [
        'GPRMC,103402.00,A,2259.73871,N,12013.40902,E,0.037,,011123,,,D*7D', 
        'GPVTG,,T,,M,0.037,N,0.069,K,D*2D', 
        'GPGGA,103402.00,2259.73871,N,12013.40902,E,2,10,0.75,27.4,M,17.2,M,,0137*60', 
        'GPGSA,A,3,28,31,16,18,27,26,03,04,08,09,,,1.39,0.75,1.18*02', 
        'GPGSV,3,1,12,03,06,234,21,04,50,293,36,08,40,213,38,09,22,313,31*7A', 
        'GPGSV,3,2,12,16,51,001,40,18,10,064,30,21,03,186,24,26,38,038,38*72', 
        'GPGSV,3,3,12,27,81,178,42,28,26,110,37,31,46,091,38,50,62,163,37*76', 
        'GPGLL,2259.73871,N,12013.40902,E,103402.00,A,D*60'
    ]
    '''
    def NMEA(self, msgs):
        print(msgs)
        for mes in msgs:
            msg = mes.split(',')
            if len(msg) < 12 or msg[0] != "GPRMC":
                continue

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
            self.status = str(msg[2])
            self.latitude = latitude_degrees
            self.latitude_hemisphere = msg[4]
            self.longitude = longitude_degrees
            self.longitude_hemisphere = msg[6]
            self.speed = msg[7]
            self.course = msg[8]
            self.date = msg[9]

            return


       
if __name__ == "__main__":
    GPS = _GPS_unit('COM6')

    while 1:
        GPS.run()
        if GPS.trigger:
            print(GPS.freq)
            print(GPS.GPS_data)

