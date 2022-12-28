#use rosbag to simulate 6 imu input at same time
#the .\fake_mutil_imu.bat

import rospy
from sensor_msgs.msg import Imu

from threading import Thread, Lock
import time

rospy.init_node("Software_Synchronization_Node", anonymous=True)
rospy.Rate(101)

ti = time.time

thread_break = False

timing_fit = False
sample_target = 0

freq_fit = False

target_timer = 0
sample_tracker = 0

p_secs, p_nsecs = 0,0

#Threading for IMU Reading by rostopic
class imu_receiver():
    def __init__(self,node_name):
        self.node_name = node_name
        self.imu_data = Imu()
        self.freq_timer = ti()
        self.freq = 0
        self.sample_num = 0
        self.init = False
        self.freq_init = False
        self.publisher_target = False
        self.trigger_times = [ti()]
        self.trigger_time = ti()
        self.trigger_add = self.trigger_times.append

    def callback(self,data):
        self.init = True
        self.imu_data = data

        if self.freq_init:
            self.sample_num += 1
            self.freq = round(self.sample_num/(ti()-self.freq_timer),2)
        else:
            self.freq_init = True
            self.freq_timer = ti()
            self.sample_num += 1

        self.trigger_time = ti()

        if self.publisher_target:
            self.sync_publisher()

    def listener(self):
        rospy.Subscriber(self.node_name, Imu, self.callback)
    
    def run(self):
        self.listener()
    
    def sync_publisher(self):
        global PUBs, IMUs, start_timer
        RIMU_data = [x.imu_data for x in IMUs]

        publish_time =  ti() - start_timer
        p_secs, p_nsecs = int(publish_time), int(publish_time*1000 % 1000)

        for x in RIMU_data:
            x.header.stamp.secs, x.header.stamp.nsecs = p_secs, p_nsecs

        [P.publish(I) for P,I in zip(PUBs,RIMU_data)]

class sync_imu_publisher():
    def __init__(self,Node_name):
        self.publisher = rospy.Publisher(Node_name, Imu, queue_size=1)

    def publish(self,IMU_data):
        self.publisher.publish(IMU_data)

IMUs = []
PUBs = []
trigger_timing = []

for i in range(5):
    IMUs.append(imu_receiver('IMU_POSE_%d'%i))
    PUBs.append(sync_imu_publisher("Sync_imu_%d"%i))
    trigger_timing.append(ti())

[x.listener() for x in IMUs]

start_timer = 0
trigger_timing_buff = []
print('init')
freq_timer = ti()

while 1:
    if not freq_fit :
        setup_time = ti() - freq_timer
        if setup_time > 5:
            print()
            print("Done.")
            freq_array = [x.freq for x in IMUs] #Read the last sample time
            print(freq_array)
            if max(freq_array) - min(freq_array) > 5:
                sample_target = int(freq_array.index(min(freq_array))) #find last imu data line
                print("the freq sample target: {}".format(sample_target))

                IMUs[sample_target].publisher_target = True
                start_timer = ti()

                freq_fit = True
                timing_fit = True

            else:
                print("The Frequency is likely, Use timing to fit")
                freq_fit = True
                timing_fit = False
        #else:
            #print("Caculating the frequency: {}  ".format(5 - int(setup_time)),end='\r')

    elif not timing_fit :
        trigger_timing = [x.trigger_times[-1] for x in IMUs] #Read the last sample time
        if not(False in [x.init for x in IMUs]):    #if there was no empty imu data
            sample_target = int(trigger_timing.index(max(trigger_timing))) #find last imu data line
            print("the sample target: {}".format(sample_target))
            timing_fit = True
            IMUs[sample_target].publisher_target = True
            start_timer = ti()
    else:
        break

rospy.spin()