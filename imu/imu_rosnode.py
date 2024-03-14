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
    rospy.init_node('IMU%d'%id, anonymous=True)
    rate = rospy.Rate(200)
    while 1:
        if rospy.is_shutdown():
            break
        IMU1.run()
        if IMU1.trigger:

            imu_header = Header()
            imu_header.seq = pub_id

            imu_header.stamp = rospy.Time.now()
            imu_header.frame_id = "world"
           
            msg = Imu()
            
            msg.header = imu_header

            msg.orientation.x = 0.0
            msg.orientation.y = 0.0
            msg.orientation.z = 0.0
            msg.orientation.w = 0.0
            msg.orientation_covariance = [99999.9, 0.0, 0.0, 0.0, 99999.9, 0.0, 0.0, 0.0, 99999.9]

            msg.angular_velocity.x ,msg.angular_velocity.y, msg.angular_velocity.z = IMU1.imu_data[1][0]*9.81, IMU1.imu_data[1][1]*9.81, IMU1.imu_data[1][2]*9.81
            msg.angular_velocity_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


            msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z = IMU1.imu_data[0][0]*9.81, IMU1.imu_data[0][1]*9.81, IMU1.imu_data[0][2]*9.81
            msg.linear_acceleration_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            pub.publish(msg)
            
            rate.sleep()

            pub_id+=1

if __name__ == '__main__':
    try:
        IMU(0)
        
    except rospy.ROSInterruptException:
        pass
