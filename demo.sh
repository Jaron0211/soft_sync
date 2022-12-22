gnome-terminal --window -e 'bash -c "sleep 0s ; roscore"' \
--tab -e 'bash -c "sleep 1s ; rosbag play imu/IMUbag/IMU_0.bag"' \
--tab -e 'bash -c "sleep 0s ; rosbag play imu/IMUbag/IMU_1.bag"' \
--tab -e 'bash -c "sleep 3s ; rosbag play imu/IMUbag/IMU_2.bag"' \
--tab -e 'bash -c "sleep 3s ; rosbag play imu/IMUbag/IMU_3.bag"' \
--tab -e 'bash -c "sleep 0s ; rosbag play imu/IMUbag/IMU_4.bag"'
gnome-terminal --window -e 'bash -c "python3 ./soft_sync.py;exec bash"'
gnome-terminal --window --title='imu_0' -e 'bash -c "rostopic echo /Sync_imu_0 -c"' \
--tab --title='imu_1' -e 'bash -c "rostopic echo /Sync_imu_1 -c"' \
--tab --title='imu_2' -e 'bash -c "rostopic echo /Sync_imu_2 -c"' \
--tab --title='imu_3' -e 'bash -c "rostopic echo /Sync_imu_3 -c"' \
--tab --title='imu_4' -e 'bash -c "rostopic echo /Sync_imu_4 -c"'
