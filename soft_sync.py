#use rosbag to simulate 6 imu input at same time
#the .\fake_mutil_imu.bat

import rospy
from sensor_msgs.msg import Imu

from threading import Thread
import time
import os
import sys

import socket 

rospy.init_node("IMUs_receiver", anonymous=True, disable_signals=False)
ti = time.time

timing_fit = False;
sample_target = 0;

#Threading for IMU Reading by rostopic
class imu_receiver(Thread):
    def __init__(self,node_name):
        Thread.__init__(self)
        self.node_name = node_name
        self.imu_data = Imu();
        self.freq_timer = ti()
        self.freq = 0
        self.sample_num = 0
        self.init = False;
        self.trigger = False
        self.trigger_times = [time.time()]
        self.trigger_add = self.trigger_times.append

    def callback(self,data):
        self.init = True;
        self.imu_data = data
        self.sample_num += 1
        self.freq = round(self.sample_num/(ti()-self.freq_timer),2)
        self.trigger_add(time.time())
        
    def listener(self):
        rospy.Subscriber(self.node_name, Imu, self.callback)
        rospy.spin()
    
    def run(self):
        self.listener()
        while 1:
            self.trigger = False;

if __name__ == '__main__':
    IMUs = []
    for i in range(5):
        IMUs.append(imu_receiver('IMU_POSE_%d'%i))
    
    [x.start() for x in IMUs]
    sample_tracker = time.time()

    loop_timer = time.time()
    total_sample = 0;

    while 1:
        if not timing_fit and (False in [x.init for x in IMUs]):
            trigger_timing = [x.trigger_times for x in IMUs]
            sample_target = int(trigger_timing.index(max(trigger_timing)))
            print("the sample target: {}".format(sample_target))
            timing_fit = True
            sample_tracker = IMUs[sample_target].trigger_times[-1]
            loop_timer = time.time()
            total_sample = 0;


        if timing_fit:
            target_timer = IMUs[sample_target].trigger_times[-1]
            if  target_timer != sample_tracker:
                
                sample_tracker = target_timer
                total_sample += 1
                #[print("{}".format(x.imu_data)) for x in IMUs]
                print(total_sample/(time.time() - loop_timer))
            else:
                print("not got sample")
            #[print("{}: {}  ".format(u.node_name,((u.trigger_times[-1])))) for u in IMUs]

        