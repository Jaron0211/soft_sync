import socket
import time 
import json
import ast
import numpy as np
import math
from vpython import *

sys_time = time.time_ns

HOST = '127.0.0.1'
PORT = 4269

#vpython var
scene = canvas()
scene2 = canvas()

scene.range=5
scene.forward=vector(-1,-1,-1)
 
scene.width=600
scene.height=600

scene2.range=5
scene2.forward=vector(-1,-1,-1)

scene2.width=600
scene2.height=600
 
xarrow=arrow(canvas=scene,lenght=2, shaftwidth=.1, color=color.red,axis=vector(1,0,0))
yarrow=arrow(canvas=scene,lenght=2, shaftwidth=.1, color=color.green,axis=vector(0,1,0))
zarrow=arrow(canvas=scene,lenght=4, shaftwidth=.1, color=color.blue,axis=vector(0,0,1))
 
frontArrow=arrow(canvas=scene2,length=2,shaftwidth=.1,color=color.purple,axis=vector(1,0,0))
upArrow=arrow(canvas=scene2,length=2,shaftwidth=.1,color=color.magenta,axis=vector(0,1,0))
sideArrow=arrow(canvas=scene2,length=2,shaftwidth=.1,color=color.orange,axis=vector(0,0,1))
 
# bBoard=box(length=6,width=2,height=.2,opacity=.8,pos=vector(0,0,0,))
# bn=box(length=1,width=.75,height=.1, pos=vector(-.5,.1+.05,0),color=color.blue)
# nano=box(lenght=1.75,width=.6,height=.1,pos=vector(-2,.1+.05,0),color=color.green)
# myObj=compound([bBoard,bn,nano])
#----

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

#f = open(str(sys_time()) + 'log_file.txt',"w+")

def unsigned_to_signed(ulong):
	iv = ulong
	if(ulong & 0b1000000000000000):
		iv = -65536 + ulong
		
	return iv

def R2Q(roll, pitch, yaw):

		qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
		qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
		qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
		qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
		return [qx, qy, qz, qw]

def imu_decoding(sensor_data):
    acc = [ #g
            unsigned_to_signed((sensor_data[0]<<8) + sensor_data[1])*(20/2**16), 
            unsigned_to_signed((sensor_data[2]<<8) + sensor_data[3])*(20/2**16),
            unsigned_to_signed((sensor_data[4]<<8) + sensor_data[5])*(20/2**16)
        ]
    #acc = [acc[0],acc[1],acc[2],0,0,0,0,0,0]
    rate = [ #rad/s
            unsigned_to_signed((sensor_data[6]<<8) + sensor_data[7])*(7*3.14/2**16),
            unsigned_to_signed((sensor_data[8]<<8) + sensor_data[9])*(7*3.14/2**16),
            unsigned_to_signed((sensor_data[10]<<8) + sensor_data[11])*(7*3.14/2**16)
        ]
    #rate = [rate[0],rate[1],rate[2],0,0,0,0,0,0]
    quat = R2Q(rate[0],rate[1],rate[2])
    #quat = [quat[0],quat[1],quat[2],quat[3],0,0,0,0,0]
    temp = [ #c
        unsigned_to_signed((sensor_data[12]<<8) + sensor_data[13])*(200/2**16),
        unsigned_to_signed((sensor_data[14]<<8) + sensor_data[15])*(200/2**16),
        unsigned_to_signed((sensor_data[16]<<8) + sensor_data[17])*(200/2**16)
    ]
    temp_b = ((sensor_data[18]<<8) + sensor_data[19])*(200/2**16) #c
    timer  = ((sensor_data[20]<<8) + sensor_data[21])*(15.259022) #uS

    BITstatus = (sensor_data[22]<<8 + sensor_data[23])

    return [acc,rate,quat,temp,temp_b,timer,BITstatus]
roll = 0.0
pitch = 0.0
yaw = 0.0
while True:
    conn, addr = s.accept()
    print('connected by ' + str(addr))

    while True:
        indata = conn.recv(1024)
        if len(indata) != 0: # connection closed
            indata = indata.decode()

            try:

                indata_list = ast.literal_eval(indata)
                title = 0

                imu_msg = indata_list[0]
                title += 1
                imu_data = imu_decoding(imu_msg)

                roll += float(imu_data[1][0])*0.01
                pitch += float(imu_data[1][1])*0.01
                yaw += float(imu_data[1][2])*0.01

                rate(100)
                k=vector(cos(yaw)*cos(pitch), sin(pitch), sin(yaw)*cos(pitch))
                y=vector(0,1,0)
                s=cross(k,y)
                v=cross(s,k)
                vrot=v*cos(roll)+cross(k,v)*sin(roll)

                frontArrow.axis=k
                sideArrow.axis=cross(k,vrot)
                upArrow.axis=vrot

                # myObj.axis=k
                # myObj.up=v
                # sideArrow.length=2
                # frontArrow.length=2
                # upArrow.length=2
                    
            except:
                  pass


        
s.close()