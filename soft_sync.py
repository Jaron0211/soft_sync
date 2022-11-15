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
    if IMU1.trigger: #if triggered, than update the imu data
        imu_data = IMU1.imu_data

    if GPS1.trigger:#if triggered, than update the GPS data
        gps_data =  GPS1.GPS_data #because the GPS freq. is the lowset, so use it as the ref freq.
        print(gps_data)
        print(imu_data)

    #to-do make it into rosnode msg

    