import rospy
from sensor_msgs.msg import Imu

import numpy as np
import pandas as pd

import time

print('init')
rospy.init_node("Recoder_Node", anonymous=True)
rospy.Rate(100)
ti = time.time

start_time = ti()
class imu_recorder():
    def __init__(self,node_id):
        
        #some basic defination
        self.node_name = node_id
        self.imu_data = Imu()
        self.timestamps = []
        self.fire_time = 0
        self.got_first = False
        self.add = self.timestamps.append

        #subscriber
        rospy.Subscriber(self.node_name, Imu, self.callback)

    def callback(self,data):
        #self.imu_data = data
        timestamp = ti() - start_time

        self.add(timestamp)

IMUs = []
for i in range(5):
    IMUs.append(imu_recorder("IMU_POSE_%d"%i))
    IMUs.append(imu_recorder('Sync_imu_%d'%i))

time.sleep(5)
# while 1:
#     if time.time() - start_time >= 5: break

save_data = pd.DataFrame([])
columns = []
for i in range(len(IMUs)):
    buff_ = pd.DataFrame(IMUs[i].timestamps)
    save_data = pd.concat([save_data,buff_],ignore_index=True,axis = 1)
    columns.append(IMUs[i].node_name)

save_data.columns = columns
save_data.to_csv('sample.csv', index=False)
print('saved')
