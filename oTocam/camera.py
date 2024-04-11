import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from std_msgs.msg import Header


def talker():
    pub = rospy.Publisher('/tutorial/image', Image, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(15)
    bridge = CvBridge()
    cap = cv2.VideoCapture()
    cap.open('/dev/video0', apiPreference=cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('U', 'Y', 'V', 'Y'))#输出图像为MJPG格式
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
    
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

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass


