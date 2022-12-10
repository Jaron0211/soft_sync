#use rosbag to simulate 6 imu input at same time
#the .\fake_mutil_imu.bat

import rospy
from sensor_msgs.msg import Imu

from threading import Thread
import time
import os
import sys

rospy.init_node("IMUs_receiver", anonymous=True, disable_signals=False)
ti = time.time

#Threading for IMU Reading by rostopic
class imu_receiver(Thread):
    def __init__(self,node_name):
        Thread.__init__(self)
        self.node_name = node_name
        self.imu_data = []
        self.freq_timer = ti()
        self.freq = 0
        self.sample_num = 0
        self.trigger = False
        self.trigger_times = []
        self.trigger_add = self.trigger_times.append

    def callback(self,data):
        self.imu_data = data
        self.sample_num += 1
        self.freq = round(self.sample_num/(ti()-self.freq_timer),2)
        self.trigger_add(time.time())
        
    def listener(self):
        rospy.Subscriber(self.node_name, Imu, self.callback)
        rospy.spin()
    
    def run(self):
        self.listener()


if __name__ == '__main__':
    IMUs = []
    for i in range(5):
        IMUs.append(imu_receiver('IMU_POSE_%d'%i))
    
    [x.start() for x in IMUs]

    while 1:
        [print("{}: {}  ".format(u.node_name,(u.freq))) for u in IMUs]
        [sys.stdout.write("\033[F") for u in IMUs]
        #time.sleep(0.1)
        
        