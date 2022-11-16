import gps.GPSbridge as gpslib
import imu.imubridge as imulib

import threading
import time

loop_freq_timer = time.time()
IMU1 = imulib._383_unit("COM5")

imu_data = []
imu_trigger = False

gps_data = []
gps_trigger = False

class threading_imu(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.IMU1 = imulib._383_unit("COM5")
    
    def run(self):
        global imu_data,imu_trigger
        while 1:
            self.IMU1.run()
            if self.IMU1.trigger:
                imu_data = self.IMU1.imu_data

class threading_gps(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.GPS1 = gpslib._GPS_unit("COM6")
    
    def run(self):
        global gps_data,gps_trigger
        while 1:
            self.GPS1.run()
            if self.GPS1.trigger:
                gps_data = self.GPS1.GPS_data

#imu = threading_imu()
gps = threading_gps()

#imu.start()
gps.start()

while 1:
    IMU1.run()

    if (gps.GPS1.trigger):
        print("IMU data: ",IMU1.imu_data)
        print("GPS data: ",gps_data)
    #time.sleep(0.005)