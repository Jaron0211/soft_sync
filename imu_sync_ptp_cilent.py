import imu.imubridge as IB
import socket

import time 

sys_time = time.time_ns()

HOST = '127.0.0.1'
PORT = 4269

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

statue_flag = []

imu_port = ["/tty/USB0","/tty/USB1","/tty/USB2"]

IMU_Units = [ IB._383_unit(i) for i in imu_port]

conn, addr = s.accept()
print('connected by ' + str(addr))

while 1:
    [ Unit.run() for Unit in IMU_Units ]

    for i in range(len(IMU_Units)):
        if Unit.trigger
            status_flag[i] = True
        
        if not(False in status_flag):
            Imu_data = [ U.raw_data for U in IMU_Units ]
            Imu_data.append(sys_time)

            send_data = str(Imu_data).encode()
            s.send(send_data)
            status_flag = [False for i in status_flag]