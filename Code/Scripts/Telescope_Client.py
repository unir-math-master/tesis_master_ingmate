#!/usr/bin/env python3

import matplotlib.pyplot as plt
import socket
import math

plt.style.use('ggplot')

HOST = '192.168.0.9'
PORT = 15556

i = 0

Accel_Range = 16384
Gyro_Range = 131

Angle1 = 0
Angle2 = 0

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    st = str(i)
    message = st.encode() 
    client.send(message)
    from_server = client.recv(255)
    client.close()

    data = from_server.decode()
    data = data.split(',')

    Accel1 = math.degrees(math.atan( -1 * (float(data[0]) / Accel_Range) / math.sqrt(math.pow( (float(data[1]) / Accel_Range), 2) + math.pow( (float(data[2]) / Accel_Range), 2))))
    Accel2 = math.degrees(math.atan(      (float(data[1]) / Accel_Range) / math.sqrt(math.pow( (float(data[0]) / Accel_Range), 2) + math.pow( (float(data[2]) / Accel_Range), 2))))
    Gyro1 = float(data[3]) / Gyro_Range
    Gyro2 = float(data[4]) / Gyro_Range
    Angle1 = 0.99*(Angle1 + Gyro1*0.0010) + 0.01*Accel2
    Angle2 = 0.99*(Angle2 + Gyro2*0.0010) + 0.01*Accel1

    print(Angle1)

    #print('Elevation:' + str(round(Angle1,10)))

    i = i+1
