#!/bin/sh
# NVIDIA Jetson TK1
# Use Gstreamer to grab H.264 video and audio stream from Logitech c920 webcam
# Preview video on screen
# Save Video and Audio to a file
# Send video as RTSP stream over TCP
# IP Address of the this machine hosting the TCP stream
IP_ADDRESS=<192.168.0.16>
# You can list devices:
# $ v4l2-ctl --list-devices
VELEM="v4l2src device=/dev/video0" #video0 is a Logitech c920 webcam with built-in H.264 compression
# Video capability from the camera - Choose One, this size will be sent out over the network
# VCAPS="video/x-h264, width=800, height=448, framerate=30/1"
# VCAPS="video/x-h264, width=1280, height=720, framerate=30/1"
VCAPS="video/x-h264, width=1920, height=1080, framerate=30/1"
# Video Source
VSOURCE="$VELEM ! $VCAPS"
# Decode the video - parse the h264 from the camera and then decode it
# Hardware accelerated by using omxh264dec
VIDEO_DEC="h264parse ! omxh264dec"
# SIZE OF THE PREVIEW WINDOW (Optional - you can remove this by modifying VIDEO_SINK)
# Here for demo purposes
PREVIEW_SCALE="video/x-raw, width=1280, height=720" 
# VIDEO_SINK is the preview window
VIDEO_SINK="videoconvert ! videoscale ! $PREVIEW_SCALE ! xvimagesink sync=false"

#AUDIO
AELEM="pulsesrc device=alsa_input.usb-046d_HD_Pro_Webcam_C920_A116B66F-02-C920.analog-stereo do-timestamp=true"
AUDIO_CAPS="audio/x-raw"
AUDIO_ENC="audioconvert ! voaacenc"
ASOURCE="$AELEM ! $AUDIO_CAPS"

# FILE_SINK is the name of the file that the video will be saved in
# File is a .mp4, Video is H.264 encoded, audio is aac encoded
FILE_SINK="filesink location=gtest1.mp4"
# Address and port to serve the video stream; check to make sure ports are available and firewalls don't block it!
TCP_SINK="tcpserversink host=$IP_ADDRESS port=5000"

#show gst-launch on the command line; can be useful for debugging
echo gst-launch-1.0 -vvv -e \
   mp4mux name=mux ! $FILE_SINK \
   $VSOURCE ! tee name=tsplit 							\
   ! queue ! $VIDEO_DEC ! $VIDEO_SINK tsplit.					\
   ! queue ! h264parse ! mux.video_0 tsplit.					\
   ! queue ! h264parse ! mpegtsmux ! $TCP_SINK					\
   $ASOURCE ! queue ! $AUDIO_ENC ! queue ! mux.audio_0
 
# first queue is for the preview
# second queue writes to the file gtest1.mp4
# third queue sends H.264 in MPEG container over TCP
gst-launch-1.0 -vvv -e \
   mp4mux name=mux ! $FILE_SINK \
   $VSOURCE ! tee name=tsplit 							\
   ! queue ! $VIDEO_DEC ! $VIDEO_SINK tsplit.					\
   ! queue ! h264parse ! mux.video_0 tsplit.					\
   ! queue ! h264parse ! mpegtsmux ! $TCP_SINK					\
   $ASOURCE ! queue ! $AUDIO_ENC ! queue ! mux.audio_0