#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()


def callback(data):
    try:
        cv_image = bridge.imgmsg_to_cv2(data)
    except CvBridgeError as e:
        print(e)

    cv2.imshow("Telescope Stream", cv_image)
    cv2.waitKey(3)


def node():
    rospy.init_node("camera_subscriber")
    image_sub = rospy.Subscriber("cameraimg", Image, callback)

    rospy.spin()


def main():
    try:
        node()
    except rospy.ROSException:
        rospy.logerr("An error occurred while trying to execute GPS")


main()
