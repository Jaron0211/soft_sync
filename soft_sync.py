#use rosbag to simulate 6 imu input at same time
#the .\fake_mutil_imu.bat

import rospy
from sensor_msgs.msg import Imu

from threading import Thread
import time
import os
import sys

import socket 

rospy.init_node("Software_Synchronization_Node", anonymous=True, disable_signals=False)
rate = rospy.Rate(101)
ti = time.time

timing_fit = False
sample_target = 0

freq_fit = False

target_timer = 0
sample_tracker = 0

#Threading for IMU Reading by rostopic
class imu_receiver(Thread):
    def __init__(self,node_name):
        Thread.__init__(self)
        self.node_name = node_name
        self.imu_data = Imu()
        self.freq_timer = ti()
        self.freq = 0
        self.sample_num = 0
        self.init = False
        self.freq_init = False
        self.trigger = False
        self.trigger_times = [ti()]
        self.trigger_time = ti()
        self.trigger_add = self.trigger_times.append

    def callback(self,data):
        if self.trigger:
            global target_timer
            target_timer = ti()

        self.init = True
        self.imu_data = data

        if self.freq_init:
            self.sample_num += 1
            self.freq = round(self.sample_num/(ti()-self.freq_timer),2)
        else:
            self.freq_init = True
            self.freq_timer = ti()
            self.sample_num += 1

        self.trigger_add(ti())
        self.trigger_time = ti()

        
    def listener(self):
        rospy.Subscriber(self.node_name, Imu, self.callback)
        rospy.spin()
    
    def run(self):
        self.listener()

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
        trigger_timing.append(ti())
    
    [x.start() for x in IMUs]

    def t():
        [P.publish(I) for P,I in zip(PUBs,RIMU_data)]

    start_timer = 0
    trigger_timing_buff = []
    print('init')
    freq_timer = ti()

    while 1:
        if not freq_fit :
            setup_time = ti() - freq_timer
            if setup_time > 15:
                print()
                print("Done.")
                freq_array = [x.freq for x in IMUs] #Read the last sample time
                print(freq_array)
                if max(freq_array) - min(freq_array) > 5:
                    sample_target = int(freq_array.index(min(freq_array))) #find last imu data line
                    print("the freq sample target: {}".format(sample_target))
                    
                    sample_tracker = IMUs[sample_target].trigger_times[-1]
                    IMUs[sample_target].trigger = True
                    start_timer = ti()

                    freq_fit = True
                    timing_fit = True
                else:
                    print("The Frequency is likely, Use timing to fit")
                    freq_fit = True
                    timing_fit = False
            else:
                print("Caculating the frequency: {}".format(15 - int(setup_time)) )

        elif not timing_fit :
            trigger_timing = [x.trigger_times[-1] for x in IMUs] #Read the last sample time
            if not(False in [x.init for x in IMUs]):    #if there was no empty imu data
                sample_target = int(trigger_timing.index(max(trigger_timing))) #find last imu data line
                print("the sample target: {}".format(sample_target))
                timing_fit = True
                sample_tracker = IMUs[sample_target].trigger_times[-1]
                IMUs[sample_target].trigger = True
                start_timer = ti()

        else:
            RIMU_data = [x.imu_data for x in IMUs]

            if  target_timer != sample_tracker:
                publish_time =  ti() - start_timer
                p_secs = int(publish_time)
                p_nsecs = int(publish_time*1000 % 1000)

                
                for x in RIMU_data:
                    x.header.stamp.secs = p_secs
                    x.header.stamp.nsecs = p_nsecs

                Thread(target = t).start()
                sample_tracker = target_timer
                #print("Publish sec: {}, nsec: {}".format(int(publish_time),int(publish_time*1000 % 1000)),end='\r')
            else:
                target_timer = IMUs[sample_target].trigger_time