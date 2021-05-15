#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from csi_camera import CSI_Camera

def node():
    rospy.init_node("camera_node_publisher")
    cvbridge = CvBridge()

    rospy.loginfo("Starting Camera .....")
    camera = CSI_Camera()
    camera.create_gstreamer_pipeline()
    camera.open(camera.gstreamer_pipeline)
    camera.start()
    rospy.loginfo("Camera  [OK]")

    publisher = rospy.Publisher('cameraimg', Image, queue_size=10)
    ros_rate = rospy.Rate(3)

    while not rospy.is_shutdown():
        _, frame = camera.read()
        if frame is not None:
            try:
                publisher.publish(cvbridge.cv2_to_imgmsg(frame, encoding="passthrough"))
            except CvBridgeError as e:
                print(e)

        ros_rate.sleep()
    
    camera.stop()


def main():
    try:
        node()
    except rospy.ROSException:
        rospy.logerr("An error occurred while trying to execute camera node")


main()