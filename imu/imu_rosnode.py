#!/usr/bin/python
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Imu

import imubridge
import time
import math

IMU1 = imubridge._383_unit('/dev/ttyUSB0')
#IMU1 = imubridge._383_unit('COM5')

pub_id = 0

def IMU(id):
    global pub_id
    pub = rospy.Publisher('IMU_POSE_%d'%id, Imu, queue_size=1)
    rospy.init_node('IMU1', anonymous=True)
    rate = rospy.Rate(100)
    while 1:
        if rospy.is_shutdown():
            break
        IMU1.run()
        if IMU1.trigger:

            imu_header = Header()
            imu_header.seq = pub_id

            time_secs = int(IMU1.timestamp/1000000)
            time_nsesc = int(IMU1.timestamp/1000)%1000

            imu_header.stamp.secs ,imu_header.stamp.nsecs = time_secs, time_nsesc
            imu_header.frame_id = "imu_frame"
           
            msg = Imu()
            
            msg.header = imu_header
            # msg.orientation.x = IMU1.imu_data[2][0]
            # msg.orientation.y = IMU1.imu_data[2][1]
            # msg.orientation.z = IMU1.imu_data[2][2]
            # msg.orientation.w = IMU1.imu_data[2][3]
            ori = msg.orientation 
            ori.x, ori.y, ori.z, ori.w = IMU1.imu_data[2][0], IMU1.imu_data[2][1], IMU1.imu_data[2][2], IMU1.imu_data[2][3]

            msg.angular_velocity.x ,msg.angular_velocity.y, msg.angular_velocity.z = IMU1.imu_data[1][0], IMU1.imu_data[1][1], IMU1.imu_data[1][2]

            msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z = IMU1.imu_data[0][0], IMU1.imu_data[0][1], IMU1.imu_data[0][2]
            pub.publish(msg)
            
            rate.sleep()

            pub_id+=1

if __name__ == '__main__':
    try:
        IMU(0)
        
    except rospy.ROSInterruptException:
        pass
