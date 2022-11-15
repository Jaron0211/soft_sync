import gps.GPSbridge as gpslib
import imu.imubridge as imulib

import serial

IMU1 = imulib._383_unit("COM5")
GPS1 = gpslib._GPS_unit("COM4")

imu_data = []
gps_data = []
while 1:
    IMU1.run()
    GPS1.run()
    if IMU1.trigger:
        imu_data = IMU1.imu_data

    if GPS1.trigger:
        gps_data =  GPS1.GPS_data
        print(gps_data)
        print(imu_data)

    