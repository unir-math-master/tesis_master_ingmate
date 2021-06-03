#!/usr/bin/python3

from mpu6050 import mpu6050

mpu = mpu6050(0x68)
mpu.set_accel_range(0x00)
mpu.set_gyro_range(0x00)

while True:
    accel_data = mpu.get_accel_data()
    gyro_data = mpu.get_gyro_data()
    temp = mpu.get_temp()

    ax = str(accel_data['x'])
    ay = str(accel_data['y'])
    az = str(accel_data['z'])
    gx = str(gyro_data['x'])
    gy = str(gyro_data['y'])
    gz = str(gyro_data['z'])
    tm = str(temp)

    #print(ax+','+ay+','+az+','+gx+','+gy+','+gz+','+tm)
    print(ax+','+ay+','+az)