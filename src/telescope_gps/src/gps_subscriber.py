#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import json


gps_data = None

def gps_callback(response):
    raw_repsonse = response.data
    if raw_repsonse != 'null':
        print(type(response.data))
        payload_data = json.loads(raw_repsonse)
        with open("gui/gps_payload.json", 'a', encoding='utf-8') as f:
            f.write(raw_repsonse+"\n")

        rospy.loginfo(f"GPS DATA: {payload_data}")


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
