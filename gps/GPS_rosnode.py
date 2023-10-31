#!/usr/bin/python
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import NavSatFix

import GPSbridge
import time
import math

GPS1 = GPSbridge._GPS_unit('/dev/ttyACM0')
#GPS1 = GPSbridge._GPS_unit('COM5')

pub_id = 1

def GPS(id, rate):
    global pub_id
    pub = rospy.Publisher('GPS_FIX_%d'%id, NavSatFix, queue_size=1)
    rospy.init_node('GPS%d'%id, anonymous=True)
    rate = rospy.Rate(rate)
    while 1:
        if rospy.is_shutdown():
            break
        GPS1.run()
        if GPS1.trigger:

            GPS_header = Header()
            GPS_header.seq = pub_id

            time_secs = int(GPS1.gps_time/1000000)
            time_nsesc = int(GPS1.gps_time/1000)%1000

            GPS_header.stamp.secs ,GPS_header.stamp.nsecs = time_secs, time_nsesc
            GPS_header.frame_id = "gps_frame"
           
            #http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html
            msg = NavSatFix()
            
            msg.header = GPS_header
            msg.status = GPS1.status
            msg.latitude = GPS1.latitude
            msg.longitude = GPS1.longitude
            msg.altitude = float('nan')
            msg.position_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            msg.position_covariance_type = msg.COVARIANCE_TYPE_KNOWN

            pub.publish(msg)
            
            rate.sleep()

            pub_id+=1

if __name__ == '__main__':
    try:
        GPS(0,100)
        
    except rospy.ROSInterruptException:
        pass