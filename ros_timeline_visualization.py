import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

sns.set_theme()

if __name__ == '__main__':
    colors = {'red': 'r', 'blue': 'b', 'green': 'g'}

    with open('sample.csv', 'r') as f:
        reader = pd.read_csv(f)
        print(reader.info())

        unsync_data = reader[['IMU_POSE_0','IMU_POSE_1','IMU_POSE_2','IMU_POSE_3','IMU_POSE_4']]
        sync_data = reader[['Sync_imu_0','Sync_imu_1','Sync_imu_2','Sync_imu_3','Sync_imu_4']]
        limt = [4,4.2]

        plt.figure('Comparision')
        fig = plt.subplot(2,1,1)
        
        sns.stripplot(data=unsync_data,dodge=True, jitter=False, orient="h")
        plt.xlim(limt)
        plt.xlabel("Time(s)")
        plt.ylabel("Sensor Topic")
        plt.title("Not synchronized")

        fig = plt.subplot(2,1,2)
        sns.stripplot(data=sync_data,dodge=True, jitter=False, orient="h")
        plt.xlim(limt)
        plt.xlabel("Time(s)")
        plt.ylabel("Sensor Topic")   
        plt.title("Synchronized")

    with open('sample.csv', 'r') as f:
        reader = pd.read_csv(f)
        plt.figure('Time error')
        unsync_data = reader[['IMU_POSE_0','IMU_POSE_1','IMU_POSE_2','IMU_POSE_3','IMU_POSE_4']]
        sync_data = reader[['Sync_imu_0','Sync_imu_1','Sync_imu_2','Sync_imu_3','Sync_imu_4']]

        for sync, unsync in zip(unsync_data, sync_data):
            print(sync, unsync)
    
    plt.show()
