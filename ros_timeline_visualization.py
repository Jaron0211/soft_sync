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
        limt = [4,4.1]

        plt.figure('Comparision 1')
        fig = plt.subplot(2,1,1)
        sns.stripplot(data=unsync_data,dodge=True, jitter=False, orient="h")
        plt.xlim(limt)

        fig = plt.subplot(2,1,2)
        sns.stripplot(data=sync_data,dodge=True, jitter=False, orient="h")
        plt.xlim(limt)

    with open('sample_2.csv', 'r') as f:
        reader = pd.read_csv(f)
        print(reader.info())

        unsync_data = reader[['IMU_POSE_0','IMU_POSE_1','IMU_POSE_2','IMU_POSE_3','IMU_POSE_4']]
        sync_data = reader[['Sync_imu_0','Sync_imu_1','Sync_imu_2','Sync_imu_3','Sync_imu_4']]
        limt = [4,4.1]

        plt.figure('Comparision 2')
        fig = plt.subplot(2,1,1)
        sns.stripplot(data=unsync_data,dodge=True, jitter=False, orient="h")
        plt.xlim(limt)

        fig = plt.subplot(2,1,2)
        sns.stripplot(data=sync_data,dodge=True, jitter=False, orient="h")
        plt.xlim(limt)
    
    plt.show()
