#Hardware driver for UART IMU
from __future__ import print_function
import sys
import os

import serial
import numpy as np
import time

imu_trigger = False
frq_timer = time.time()

package_types = {
	#Link test
	"504b":"PK",
	"4348":"CH",
	#Interactive Commands
	"4750":"GP",
	"1515":"NAK",
	#Output Messages: Status & Other, (Polled Only)
	"4944":"ID",
	"5652":"VR",
	"5430":"T0",
	#Output Messages: Measurement Data (Continuous or Polled)
	"5330":"S0",
	"5331":"S1",
	#Advanced Commands
	"5746":"WF",
	"5346":"SF",
	"5246":"RF",
	"4746":"GF"
}

def unsigned_to_signed(ulong):
	iv = ulong
	if(ulong & 0b1000000000000000):
		iv = -65536 + ulong
		
	return iv

class _383_unit():

	def __init__(self,port):
		
		self.ser = serial.Serial(port,115200,parity=serial.PARITY_NONE, rtscts=1,timeout=0.001)
		if self.ser.is_open:
			self.ser.close()

		self.ser.open()
		
		self._header_buffer = []
		self._buffer = []
		self.header_check = False
		self.imu_data = [[0,0,0],[0,0,0],[0,0,0],0,0,0]
		self.timestamp = 0
		self.ser.flush()
		
		self.shift_mean_frq = 0
		self.imu_frq_timer = 0
		self.first_header = False
		self.second_header = False
		self.trigger = False

		self.raw_data = ''
	
	def R2Q(self,roll, pitch, yaw):

		qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
		qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
		qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
		qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
		return [qx, qy, qz, qw]

	def run(self):
		global frq_timer
		if self.first_header and self.second_header:
			_type = self.ser.read(size = 2)
			_length = self.ser.read(size = 1)

			if _type == b'S1':

				sensor_data = self.ser.read(size = ord(_length))
				
				try:
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
					quat = self.R2Q(rate[0],rate[1],rate[2])
					#quat = [quat[0],quat[1],quat[2],quat[3],0,0,0,0,0]
					temp = [ #c
						unsigned_to_signed((sensor_data[12]<<8) + sensor_data[13])*(200/2**16),
						unsigned_to_signed((sensor_data[14]<<8) + sensor_data[15])*(200/2**16),
						unsigned_to_signed((sensor_data[16]<<8) + sensor_data[17])*(200/2**16)
					]
					temp_b = ((sensor_data[18]<<8) + sensor_data[19])*(200/2**16) #c
					timer  = ((sensor_data[20]<<8) + sensor_data[21])*(15.259022) #uS
					
					time_delta = timer - self.imu_frq_timer
					
					if time_delta >= 0:
						self.timestamp += time_delta
					else:
						self.timestamp += (1000000+time_delta)


					BITstatus = (sensor_data[22]<<8 + sensor_data[23])
												
					self.imu_data = [acc,rate,quat,temp,temp_b,self.timestamp,BITstatus]

					self.shift_mean_frq = (1/(timer-self.imu_frq_timer+0.00001)*1000000)
					self.imu_frq_timer = timer
				except IndexError as err:
					pass
				self.second_header = False
				self.first_header = False
				self.trigger = True

				self.raw_data = sensor_data
				self.ser.flush()
			else:
				self.second_header = False
				self.first_header = False
		
		else:
			self.trigger = False
			_buf = self.ser.read(size = 1)
			if (_buf) == b'U' and not self.first_header:
				self.first_header = True
			
			elif (_buf) == b'U' and self.first_header:
				self.second_header = True
			
			else:
				self.second_header = False
				self.first_header = False
				


if "__main__" == __name__:
	IMU1 = _383_unit('/dev/ttyUSB0')

	while(1):
		IMU1.run()

		if IMU1.trigger:

			data = IMU1.imu_data
			output = (
				"ACC_X: %4f ACC_Y: %4f ACC_Z: %4f"%(data[0][0],data[0][1],data[0][2]),
				"q_X: %4f q_Y: %4f q_Z: %4f q_W: %4f"%(data[2][0],data[2][1],data[2][2],data[2][3]),
				"GYRO_X: %4f GYRO_Y: %4f GYRO_Z: %4f"%(data[1][0],data[1][1],data[1][2]),
				"temp_X: %4f temp_Y: %4f temp_Z: %4f"%(data[3][0],data[3][1],data[3][2]),
				"board temp: %4f"%data[4],
				"timestamp: %d"%data[5],
				"Bitstate: %d"%data[6],
				"frequence: %2f"%IMU1.shift_mean_frq
				)
			
			#print(output)
			#print("frequence: %2f"%IMU1.shift_mean_frq)
			#print("timer: %.4f"%(IMU1.imu_data[5]/1000000))
			#sys.stdout.flush()
			#os.system('cls')
