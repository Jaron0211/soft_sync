### IMU
For imu383ZA with USB adapter(in UART mode) 

### GPS
Simple UART lib(NMEA format)

---
### This project is test on Windows 10 ,ROS noetic(u can find the ROS installation on the ROS official website http://wiki.ros.org/Installation/Windows)

### IMU
For imu383ZA with USB adapter(in UART mode), the driver file is ./imu/imubridge.py
to emulate multi-imu inputs, we use rosbag to log the sensor info, and play all 5 file simultaneously.

./imu/imu_rosnode.py is a simple example for imu2rosnode program.

./imu/IMUbag folder contain with 5 record file(~5mins record).

And with ROS environment, run the fake_multi_imu.bat to play all the bag files at the same time.


### GPS
Simple UART lib(NMEA format), the driver file is ./gps/GPSbridge.py

ROS.lnk file is the example shortcut file that run cmd with the ROS environment.
hardware_soft_sync.py do the hardware level sychonization, 
soft_sync.py run with ROS, it's for Synchronize every ROS node data.(ref. paper: /cites/A_Soft_Time_Synchronization_Framework_for_Multi-Sensors_in_Autonomous_Localization_and_Navigation.pdf)
