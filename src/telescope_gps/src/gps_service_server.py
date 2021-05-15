#!/usr/bin/env python3
import rospy
from telescope_gps.srv import gps, gpsResponse
from std_msgs.msg import String
from gps import GPSTelescope
import json
import yaml
from pathlib import Path


def get_config():
    config_file = query_file = Path(__file__).parent / 'config.yaml'
    yaml_config = open(config_file, 'r')
    return yaml.load(yaml_config)

def gps_response():
    return gpsResponse("{'gps_data':'ok'}")

def node():
    rospy.init_node("gps_server_node")
    config = get_config()

    server = rospy.Service("gps_service", gps, gps_response)

    rospy.loginfo("GPS Service.....[OK]")
    rospy.spin()


def main():
    try:
        node()
    except rospy.ROSException:
        rospy.logerr("An error occurred while trying to excecute GPS service")


main()