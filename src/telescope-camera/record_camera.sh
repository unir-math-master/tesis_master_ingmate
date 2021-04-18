SENSOR_ID=0 # 0 for CAM0 and 1 for CAM1 ports
FRAMERATE=30 # Framerate can go from 2 to 30 for 4032x3040 mode
gst-launch-1.0 -e nvarguscamerasrc sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=4032,height=3040,framerate=$FRAMERATE/1" ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=rpi_v3_imx477_cam$SENSOR_ID.mp4