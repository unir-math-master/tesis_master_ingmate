# ROS

## Create ROS package
```
cd /src
catkin_create_pkg <name> rospy std_msgs message_generation actionlib actionlib_msgs
```
### Build the package
```
catkin_make
source devel/setup.bash
```