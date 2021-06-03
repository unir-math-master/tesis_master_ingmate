#!/usr/bin/python3

from mpu6050 import mpu6050
from bmp180 import bmp180
from time import sleep

import mysql.connector
import smbus
import math
import socket
import smbus

ingmate_bdd = mysql.connector.connect(user='jbalsells', password='12345678', host='127.0.0.1', database='unir_ingmate')
cursor = ingmate_bdd.cursor()

port = 15556

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', port))

sensor = mpu6050(0x68)
sensor.set_accel_range(0x00)
sensor.set_gyro_range(0x00)

bmp = bmp180(0x77)

bus = smbus.SMBus(1)
bus.write_byte_data(0x68, 0x37, 0x02)
bus.write_byte_data(0x68, 0x6A, 0x00)

bus.write_byte_data(0x1E, 0x00, 0xF8)
bus.write_byte_data(0x1E, 0x01, 0xE0)
bus.write_byte_data(0x1E, 0x02, 0x00)
sleep(0.5)

Declination = 0.67#0.67° E  ± 0.33°  changing by  0.12° W per year
#https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml

i=0

def database():
    cursor.execute("SHOW TABLES")
    myresult = cursor.fetchall()

    print(myresult)

def read_sensors():
    pass

try:
    while True:
        socket.listen(5)
        client, address = socket.accept()
        print("Connected to %s on port %s" % (address, port))

        accel_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        temp = sensor.get_temp()

        ax = str(accel_data['x'])
        ay = str(accel_data['y'])
        az = str(accel_data['z'])
        gx = str(gyro_data['x'])
        gy = str(gyro_data['y'])
        gz = str(gyro_data['z'])
        t1 = str(temp)

        t2 = str(bmp.get_temp())
        pr = str(bmp.get_pressure())
        al = str(bmp.get_altitude())

        data = bus.read_i2c_block_data(0x1E, 0x03, 6)
        xMag = data[0] * 256 + data[1]
        if xMag > 32767 :
            xMag -= 65536
        zMag = data[2] * 256 + data[3]
        if zMag > 32767 :
            zMag -= 65536
        yMag = data[4] * 256 + data[5]
        if yMag > 32767 :
            yMag -= 65536
        azim = math.atan2(yMag,xMag)
        azim = math.degrees(azim)    
        azim = str(azim)

        response = client.recv(255)
        if response != "":
                print(response)

        st = ax+','+ay+','+az+','+gx+','+gy+','+gz+','+t1+','+t2+','+pr+','+al+','+azim
        print(st)
        message = st.encode()        
        client.send(message)   
        sleep(0.00005)         

        file_object = open('mpu6050.txt', 'a')
        file_object.write(str(i) + ',' + str(accel_data['x']) + '\r\n')
        file_object.close()

        i = i+1


except KeyboardInterrupt:
    client.close()
    socket.close()
    cursor.close()
    ingmate_bdd.close()

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    pass