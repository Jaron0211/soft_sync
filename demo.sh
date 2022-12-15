{
gnome-terminal --window -- bash -c "sleep 0s ; roscore"
}&

sleep 5s
{
gnome-terminal --window -- bash -c "rosbag play imu/IMUbag/IMU_0.bag" 
gnome-terminal --tab -- bash -c "rosbag play imu/IMUbag/IMU_1.bag"
gnome-terminal --tab -- bash -c "rosbag play imu/IMUbag/IMU_2.bag"
gnome-terminal --tab -- bash -c "rosbag play imu/IMUbag/IMU_3.bag"
gnome-terminal --tab -- bash -c "rosbag play imu/IMUbag/IMU_4.bag"
}&

gnome-terminal --tab -- bash -c 'python3 sofy_sync.py'

sleep 7s
{
gnome-terminal --window -- bash -c 'rostopic echo /Sync_imu_0 -c'
gnome-terminal --tab -- bash -c 'rostopic echo /Sync_imu_1 -c'
gnome-terminal --tab -- bash -c 'rostopic echo /Sync_imu_2 -c'
gnome-terminal --tab -- bash -c 'rostopic echo /Sync_imu_3 -c'
gnome-terminal --tab -- bash -c 'rostopic echo /Sync_imu_4 -c'
gnome-terminal --tab -- bash -c 'rostopic echo /Sync_imu_5 -c'
}
