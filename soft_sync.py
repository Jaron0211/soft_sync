import gps.GPSbridge as gpslib
import imu.imubridge as imulib

import threading
import time
import os

loop_freq_timer = time.time()
IMU1 = imulib._383_unit("COM5")

imu_data = []
imu_trigger = False

gps_data = []
gps_trigger = False

# class threading_imu(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.IMU1 = imulib._383_unit("COM5")
#     def run(self):
#         global imu_data,imu_trigger
#         while 1:
#             self.IMU1.run()
#             if self.IMU1.trigger:
#                 imu_data = self.IMU1.imu_data

class threading_gps(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.GPS1 = gpslib._GPS_unit("COM6")
        self.GPS_sample_time = time.time()
    
    def run(self):
        global gps_data,gps_trigger
        while 1:
            self.GPS1.run()
            if self.GPS1.trigger:
                self.GPS_sample_time = time.time()
                gps_data = self.GPS1.GPS_data

gps = threading_gps()

loop_timer = time.time()
gps.start()

while 1:
    IMU1.run()

    if (gps.GPS1.trigger):
        os.system('cls')
        print("IMU data: ")
        data = IMU1.imu_data
        output = (
				"ACC_X: %4f ACC_Y: %4f ACC_Z: %4f"%(data[0][0],data[0][1],data[0][2]),
				"q_X: %4f q_Y: %4f q_Z: %4f q_W: %4f"%(data[2][0],data[2][1],data[2][2],data[2][3]),
				"GYRO_X: %4f GYRO_Y: %4f GYRO_Z: %4f"%(data[1][0],data[1][1],data[1][2]),
				"temp_X: %4f temp_Y: %4f temp_Z: %4f"%(data[3][0],data[3][1],data[3][2]),
				"board temp: %4f"%data[4],
				"timestamp: %d"%data[5],
				"Bitstate: %d"%data[6],
				"frequence: %2f"%IMU1.shift_mean_frq
				)
        for i in output:
            print(i)
        #print("IMU freq: ",IMU1.shift_mean_frq)
        print()
        print("GPS data: ")
        for i in gps_data:
            print(i)
        print("GPS freq: ",gps.GPS1.freq)
        print()
        print("msg freq: ",1/(time.time() - loop_timer))
        print("取樣與輸出誤差時間: {} s".format(round(time.time() - gps.GPS_sample_time,4)))
        loop_timer = time.time()
