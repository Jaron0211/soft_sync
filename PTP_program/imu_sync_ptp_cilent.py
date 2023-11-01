import imu.imubridge as IB
import socket
import time 

HOST = '127.0.0.1'
PORT = 4269

imu_port = ["/dev/ttyUSB0","/dev/ttyUSB1"]

sys_time = time.time_ns
status_flag = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#initialization
IMU_Units = [ IB._383_unit(i) for i in imu_port]

for i in range(len(IMU_Units)):
    status_flag.append(False)

while 1:
    [ Unit.run() for Unit in IMU_Units ]

    for U,F in zip(IMU_Units,status_flag):
        if U.trigger and len(U.imu_data)>3:
            status_flag[F] = True

    if not(False in status_flag):
        Imu_data = [ U.raw_data for U in IMU_Units ]
        Imu_data.append(sys_time())

        send_data = str(Imu_data).encode()
        s.send(send_data)
        status_flag = [False for i in status_flag]