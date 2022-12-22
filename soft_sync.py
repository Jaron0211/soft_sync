#use rosbag to simulate 6 imu input at same time
#the .\fake_mutil_imu.bat

import rospy
from sensor_msgs.msg import Imu

from threading import Thread
import time
import os
import sys

import socket 

rospy.init_node("Synchronization_Node", anonymous=True, disable_signals=False)
rate = rospy.Rate(100)
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

class sync_imu_publisher():
    def __init__(self,Node_name):
        self.publisher = rospy.Publisher(Node_name, Imu, queue_size=10)
    
    def publish(self,IMU_data):
        self.publisher.publish(IMU_data)
        
        

if __name__ == '__main__':
    IMUs = []
    PUBs = []
    trigger_timing = []
    for i in range(5):
        IMUs.append(imu_receiver('IMU_POSE_%d'%i))
        PUBs.append(sync_imu_publisher("Sync_imu_%d"%i))
        trigger_timing.append(time.time())
    
    [x.start() for x in IMUs]
    

    start_timer = 0
    trigger_timing_buff = []
    print('init')
    while 1:
        
        if not timing_fit :
            trigger_timing = [x.trigger_times[-1] for x in IMUs]
            if not(False in [x.init for x in IMUs]):    
                sample_target = int(trigger_timing.index(max(trigger_timing)))
                print("the sample target: {}".format(sample_target))
                timing_fit = True
                sample_tracker = IMUs[sample_target].trigger_times[-1]
                start_timer = time.time()
            
            if trigger_timing != trigger_timing_buff:
                print(trigger_timing)
                print()
                trigger_timing_buff = trigger_timing


        if timing_fit:
            target_timer = IMUs[sample_target].trigger_times[-1]
            if  target_timer != sample_tracker:

                sample_tracker = target_timer

                publish_time = time.time() - start_timer

                RIMU_data = [x.imu_data for x in IMUs]
                for x in RIMU_data:
                    x.header.stamp.secs = int(publish_time)
                    x.header.stamp.nsecs = int(publish_time*1000 % 1000)
                    
                [P.publish(I) for P,I in zip(PUBs,RIMU_data)]
                #print("Publish sec: {}, nsec: {}".format(int(publish_time),int(publish_time*1000 % 1000)))
                #sys.stdout.flush()