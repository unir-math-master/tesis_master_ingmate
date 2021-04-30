#!/usr/bin/env python3
import rospy
from std_msgs.msg import String


def gps_callback(response):
    rospy.loginfo(f"GPS DATA: {response.data}")


def node():
    rospy.init_node("gps_subscriber")
    rospy.loginfo("GPS Subscriber started ....... [OK]")
    rospy.Subscriber('gpsdata', String, gps_callback)

    rospy.spin()


def main():
    try:
        node()
    except rospy.ROSException:
        rospy.logerr("An error occurred while trying to execute GPS")


main()
