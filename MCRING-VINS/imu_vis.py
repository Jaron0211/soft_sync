import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import serial
import numpy as np
import time

from datetime import timezone 
import datetime 
import os, sys

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
		
		self.received_timestamp = 0
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

		self.first_msg = True
		self.aligned_timer = time.time()

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

			if self.first_msg:
				self.aligned_timer = int(datetime.datetime.now(datetime.timezone.utc).timestamp()*1000000)
				self.first_msg = False

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
												
					self.imu_data = [acc,rate,quat,temp,temp_b,self.aligned_timer + self.timestamp,BITstatus]

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
class IMUPlotter:
    def __init__(self, IMU, max_length=200):
        self.IMU = IMU
        self.fig, self.axs = plt.subplots(2, 1, figsize=(10, 8))
        self.max_length = max_length
        self.x_data = np.linspace(0, max_length-1, max_length)
        self.acc_data = np.zeros((3, max_length))
        self.gyro_data = np.zeros((3, max_length))
        
        self.acc_lines = [self.axs[0].plot(self.x_data, self.acc_data[i], label=f'ACC_{axis}')[0] for i, axis in enumerate(['X', 'Y', 'Z'])]
        self.gyro_lines = [self.axs[1].plot(self.x_data, self.gyro_data[i], label=f'GYRO_{axis}')[0] for i, axis in enumerate(['X', 'Y', 'Z'])]
        
        self.axs[0].set_title('Accelerometer')
        self.axs[0].legend()
        self.axs[1].set_title('Gyroscope')
        self.axs[1].legend()
        
        for ax in self.axs:
            ax.set_xlim(0, max_length-1)
            ax.set_ylim(-10, 10)  # Adjust these limits based on your expected sensor values
        
    def update_plot(self, frame):
        acc, gyro, _, _, _,_= self.IMU.imu_data
        self.acc_data = np.roll(self.acc_data, -1, axis=1)
        self.acc_data[:, -1] = acc
        self.gyro_data = np.roll(self.gyro_data, -1, axis=1)
        self.gyro_data[:, -1] = gyro
        
        for i in range(3):
            self.acc_lines[i].set_ydata(self.acc_data[i])
            self.gyro_lines[i].set_ydata(self.gyro_data[i])
        return self.acc_lines + self.gyro_lines

if "__main__" == __name__:
    IMU1 = _383_unit('/dev/ttyUSB0')
    plotter = IMUPlotter(IMU1)
    
    # Animation
    ani = FuncAnimation(plotter.fig, plotter.update_plot, blit=True, interval=50)
    
    plt.show()
