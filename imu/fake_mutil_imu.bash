gnome-terminal --tab -- 'bash -c "sleep 0s ; roscore ;exec bash"'
gnome-terminal --tab -- 'bash -c "sleep 5s ; rosbag play ./IMUbag/IMU_0.bag;exec bash"'
gnome-terminal --tab -- 'bash -c "sleep 5s ; rosbag play ./IMUbag/IMU_1.bag;exec bash"'
gnome-terminal --tab -- 'bash -c "sleep 5s ; rosbag play ./IMUbag/IMU_2.bag;exec bash"'
gnome-terminal --tab -- 'bash -c "sleep 5s ; rosbag play ./IMUbag/IMU_3.bag;exec bash"'
gnome-terminal --tab -- 'bash -c "sleep 5s ; rosbag play ./IMUbag/IMU_4.bag;exec bash"'

