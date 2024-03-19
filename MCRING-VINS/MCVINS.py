import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from std_msgs.msg import Header

import imubridge
from std_msgs.msg import Header
from sensor_msgs.msg import Imu

import threading

IMU1 = imubridge._383_unit('/dev/ttyUSB0')

pub_id = 0

def talker():
    pub = rospy.Publisher('/tutorial/image', Image, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(15)
    bridge = CvBridge()
    cap = cv2.VideoCapture()
    cap.open('/dev/video0', apiPreference=cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('U', 'Y', 'V', 'Y'))#输出图像为MJPG格式
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)#修改图像宽度为1920
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)#修改图像高度为1080
    
    while not rospy.is_shutdown():
        ret, img = cap.read()
        if ret:  # 检查图像是否成功读取
            img = cv2.resize(img,(960,640))
            rotated_video = cv2.rotate(img, cv2.ROTATE_180)
            # cv2.imshow("talker", rotated_video)
            # cv2.waitKey(1)

            header = Header()
            header.stamp = rospy.Time.now()
            ros_img = bridge.cv2_to_imgmsg(rotated_video, "bgr8")
            ros_img.header = header
            pub.publish(ros_img)
        else:
            rospy.logwarn("Failed to read frame from camera.")
        rate.sleep()

def IMU(id):
    global pub_id
    pub = rospy.Publisher('IMU_POSE_%d'%id, Imu, queue_size=1)
    rospy.init_node('IMU%d'%id, anonymous=True)
    rate = rospy.Rate(200)
    while 1:
        if rospy.is_shutdown():
            break
        IMU1.run()
        if IMU1.trigger:

            imu_header = Header()
            imu_header.seq = pub_id

            imu_header.stamp = rospy.Time.now()
            imu_header.frame_id = "world"
           
            msg = Imu()
            
            msg.header = imu_header

            msg.orientation.x = 0.0
            msg.orientation.y = 0.0
            msg.orientation.z = 0.0
            msg.orientation.w = 0.0
            msg.orientation_covariance = [99999.9, 0.0, 0.0, 0.0, 99999.9, 0.0, 0.0, 0.0, 99999.9]

            msg.angular_velocity.x ,msg.angular_velocity.y, msg.angular_velocity.z = IMU1.imu_data[1][0]*9.81, IMU1.imu_data[1][1]*9.81, IMU1.imu_data[1][2]*9.81
            msg.angular_velocity_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


            msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z = IMU1.imu_data[0][0]*9.81, IMU1.imu_data[0][1]*9.81, IMU1.imu_data[0][2]*9.81
            msg.linear_acceleration_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            pub.publish(msg)
            
            rate.sleep()

            pub_id+=1

cam_thread = threading.Thread(taget=talker)
imu_thread = threading.Thread(taget=IMU,0)

if __name__ == '__main__':
    try:
        cam_thread.start()
        imu_thread.start()
    except rospy.ROSInterruptException:
        pass


