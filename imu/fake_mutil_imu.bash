gnome-terminal --tab -- bash -c 'sleep 0s ; roscore'
gnome-terminal --tab -- bash -c 'sleep 5s ; rosbag play ./IMUbag/IMU_0.bag'
gnome-terminal --tab -- bash -c 'sleep 5s ; rosbag play ./IMUbag/IMU_1.bag'
gnome-terminal --tab -- bash -c 'sleep 5s ; rosbag play ./IMUbag/IMU_2.bag'
gnome-terminal --tab -- bash -c 'sleep 5s ; rosbag play ./IMUbag/IMU_3.bag'
gnome-terminal --tab -- bash -c 'sleep 5s ; rosbag play ./IMUbag/IMU_4.bag'

