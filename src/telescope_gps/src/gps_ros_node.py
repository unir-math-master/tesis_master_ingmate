#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from gps import GPSTelescope
import json
import yaml
from pathlib import Path


def get_config():
    config_file = query_file = Path(__file__).parent / 'config.yaml'
    yaml_config = open(config_file, 'r')
    return yaml.load(yaml_config)

def node():
    rospy.init_node("gps_node_publisher")
    config = get_config()

    rospy.loginfo("Starting GPS node ....")
    telescope_gps = GPSTelescope(config['serial_port'])

    publisher = rospy.Publisher('gpsdata', String, queue_size=config['queue_size'])
    ros_rate = rospy.Rate(config['ros_rate'])

    rospy.loginfo("Gettig GPS Data ....")
    while not rospy.is_shutdown():
        gps_data = json.dumps(telescope_gps.get_gps_data())
        rospy.loginfo(gps_data)
        publisher.publish(gps_data)
        ros_rate.sleep()

def main():
    try:
        node()
    except rospy.ROSException:
        rospy.logerr("An error ocurred while trying to excecute GPS")


main()