#!/usr/bin/env python3

from gps import GPSTelescope
import rospy

SERIAL_PORT = "/dev/ttyUSB0"

def node():
    rospy.init_node("gps_node")
    rospy.loginfo("Starting GPS node ....")
    telescope_gps = GPSTelescope(SERIAL_PORT)
    rospy.loginfo("Gettig GPS Data ....")
    telescope_gps.get_gps_data()

def main():

    try:
        node()
    except rospy.ROSException:
        print("An error ocurred while trying to excecute GPS")


main()