#use rosbag to simulate 6 imu input at same time
#the .\fake_mutil_imu.bat

import pandas as pd

import rospy
from sensor_msgs.msg import Imu

from threading import Thread, Lock
import time

from pympler.asizeof import asizeof

rospy.init_node("Software_Synchronization_Node", anonymous=True)

ti = time.time

thread_break = False

timing_fit = False
sample_target = 0

freq_fit = False

target_timer = 0
sample_tracker = 0

p_secs, p_nsecs = 0,0

timmimg_array = []

#Threading for IMU Reading by rostopic
class imu_receiver():
    def __init__(self,node_id):
        
        #some basic defination
        self.node_name = 'IMU_POSE_%d'%node_id
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
        self.start_timer = ti()
        self.last_pub = ti()
        
        #subscriber
        rospy.Subscriber(self.node_name, Imu, self.callback)

        #publisher
        self.publisher = rospy.Publisher('Sync_imu_%d'%node_id, Imu, queue_size=3)
        self.pub = self.publisher.publish


    def callback(self,data):
        
        self.init = True
        self.imu_data = data

        self.publish_time =  ti() - self.start_timer
        #p_secs, p_nsecs = int(publish_time), int(publish_time*1000 % 1000)

        buff_ = self.imu_data.header.stamp
        buff_.secs, buff_.nsecs = int(self.publish_time), int(self.publish_time*1000 % 1000)

        self.sample_num += 1
        if not self.freq_init: self.freq_init = True; self.freq_timer = ti()

        self.trigger_time = ti()
        self.trigger_add(self.trigger_time)

        if self.publisher_target:
            global IMUs
            [I.sync_publisher() for I in IMUs]; self.last_pub = ti(); timmimg_array.append([I.trigger_time for I in IMUs])

    def sync_publisher(self):
        self.pub(self.imu_data)
        #print(asizeof(self.imu_data))

IMUs = []
trigger_timing = []

for i in range(5):
    IMUs.append(imu_receiver(i))
    trigger_timing.append(ti())

start_timer = 0
trigger_timing_buff = []
print('init')
freq_timer = ti()

for iter in range(5):
    if not freq_fit :
        setup_time = ti() - freq_timer
        time.sleep(5)
        print()
        print("Done.")

        freq_array = [round(x.sample_num/(ti()-x.freq_timer),2) for x in IMUs] #Read the last sample time
        print(freq_array)
        if max(freq_array) - min(freq_array) > 1:
            sample_target = int(freq_array.index(min(freq_array))) #find last imu data line

            print("the freq sample target: {}".format(sample_target))

            IMUs[sample_target].publisher_target = True

            start_timer = ti()
            for I in IMUs:
                I.start_timer = start_timer

            freq_fit = True
            timing_fit = True

        else:
            print("The Frequency is likely, Use timing to fit")
            freq_fit = True
            timing_fit = False
        #else:
            #print("Caculating the frequency: {}  ".format(5 - int(setup_time)),end='\r')

    elif not timing_fit :
        if not(False in [x.init for x in IMUs]):    #if there was no empty imu data

            #trigger_timing = [x.trigger_times[-1] for x in IMUs] #Read the last sample time
            #sample_target = int(trigger_timing.index(max(trigger_timing))) #find last imu data line
            IMUs_buffer = [X.trigger_times for X in IMUs]
            minimun_time = 100
            sample_target = 0

            for I_1_num in range(len(IMUs_buffer)):
                #print("o1",I_1_num)
                I_1 = IMUs_buffer[I_1_num]

                m1_point = I_1[-20]
                error_array = []

                for I_2_num in range(len(IMUs_buffer)):
                    #print("o2",I_2_num)

                    I_2 = IMUs_buffer[I_2_num]
                    this_error_sequence = [m1_point - T for T in I_2]
                    #print(this_error_sequence)
                    for tt in range(len(this_error_sequence)):
                        if this_error_sequence[tt] < 0 :
                            error_array.append(this_error_sequence[tt-1])
                            #print(this_error_sequence[tt-2],this_error_sequence[tt-1],this_error_sequence[tt])
                            break
                print(error_array)
                the_error_sum = sum(error_array)
                print("{}'s error time: {}, error array: {}".format(I_1_num,the_error_sum,error_array))
                if the_error_sum < minimun_time:
                    sample_target = I_1_num
                    minimun_time = the_error_sum


            print("the sample target: {}".format(sample_target))
            timing_fit = True
            IMUs[sample_target].publisher_target = True
            start_timer = ti()
            break
        else:
            break

while 1:
    time.sleep(1)
    try:
        pd.DataFrame(timmimg_array).to_csv('log.csv')
    except:
        continue

rospy.spin()
