gnome-terminal --window -e 'bash -c "sleep 0s ; roscore"' \
--tab -e 'bash -c "sleep 0s ; rosbag play imu/IMUbag/IMU_0.bag"' \
--tab -e 'bash -c "sleep 0s ; rosbag play imu/IMUbag/IMU_1.bag"' \
--tab -e 'bash -c "sleep 0s ; rosbag play imu/IMUbag/IMU_2.bag"' \
--tab -e 'bash -c "sleep 0s ; rosbag play imu/IMUbag/IMU_3.bag"' \
--tab -e 'bash -c "sleep 0s ; rosbag play imu/IMUbag/IMU_4.bag"'
gnome-terminal --window -e 'bash -c "sleep 2s ; rosbag record /IMU_POSE_0 /IMU_POSE_1 /IMU_POSE_2 /IMU_POSE_3 /IMU_POSE_4"' \
