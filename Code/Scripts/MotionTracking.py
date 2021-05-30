#!/usr/bin/python3
#sudo i2cdetect -y -r 0
#sudo i2cdetect -y -r 1

import numpy as np
import matplotlib as plt
from mpu6050 import mpu6050
from time import sleep

sensor = mpu6050(0x68)
sensor.set_accel_range(0x00)
sensor.set_gyro_range(0x00)

i=0

while True:
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    temp = sensor.get_temp()

    #print("Accelerometer data")
    #print("x: " + str(accel_data['x']))
    #print("y: " + str(accel_data['y']))
    #print("z: " + str(accel_data['z']))

    #print("Gyroscope data")
    #print("x: " + str(gyro_data['x']))
    #print("y: " + str(gyro_data['y']))
    #print("z: " + str(gyro_data['z']))

    #print("Temp: " + str(temp) + " C")

    ax = str(accel_data['x'])
    ay = str(accel_data['y'])
    az = str(accel_data['z'])
    gx = str(gyro_data['x'])
    gy = str(gyro_data['y'])
    gz = str(gyro_data['z'])
    tm = str(temp)

    print(ax+','+ay+','+az+','+gx+','+gy+','+gz+','+tm)
    sleep(0.001)

    file_object = open('mpu6050.txt', 'a')
    file_object.write(str(i) + ',' + str(accel_data['x']) + '\r\n')
    file_object.close()

    i = i+1
