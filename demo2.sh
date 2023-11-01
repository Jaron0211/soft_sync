gnome-terminal --window -e 'bash -c "sleep 0s ; roscore"' \
--tab -e 'bash -c "sleep 0s ; rosbag play replay.bag ;exec bash"'
gnome-terminal --window -e 'bash -c "sleep 3s ; python3 ./soft_sync.py ;exec bash"' \
--tab --title='imu_1_hz' -e 'bash -c "sleep 3s ; rostopic hz /Sync_imu_1"' \
--tab --title='imu_2_hz' -e 'bash -c "sleep 3s ; rostopic hz /Sync_imu_2"' \
--tab --title='imu_3_hz' -e 'bash -c "sleep 3s ; rostopic hz /Sync_imu_3"' \
--tab --title='imu_4_hz' -e 'bash -c "sleep 3s ; rostopic hz /Sync_imu_4"' \
--tab --title='imu_0_hz' -e 'bash -c "sleep 3s ; rostopic hz /Sync_imu_0"'
gnome-terminal --window --title='imu_0' -e 'bash -c "rostopic echo /Sync_imu_0 -c"' \
--tab --title='imu_1' -e 'bash -c "rostopic echo /Sync_imu_1 -c"' \
--tab --title='imu_2' -e 'bash -c "rostopic echo /Sync_imu_2 -c"' \
--tab --title='imu_3' -e 'bash -c "rostopic echo /Sync_imu_3 -c"' \
--tab --title='imu_4' -e 'bash -c "rostopic echo /Sync_imu_4 -c"'
gnome-terminal --window --title='recoeder' -e 'bash -c "sleep 10s ; python3 ./ros_timeline_recorder.py"'
gnome-terminal --window --title='recoeder' -e 'bash -c "sleep 16s ; python3 ./ros_timeline_visualization.py ;exec bash"'
