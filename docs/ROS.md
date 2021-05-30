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

If we get this error `Unable to find either executable 'empy' or Python module 'em'` after excecute `catkin_make`, whe need to install empy package
```
pip3 install empy
```
