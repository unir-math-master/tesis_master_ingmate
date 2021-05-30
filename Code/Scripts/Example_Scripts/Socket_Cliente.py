#!/usr/bin/env python3

import socket

HOST = '192.168.0.16'
PORT = 15556

i = 0

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    st = str(i)
    message = st.encode() 
    client.send(message)
    from_server = client.recv(255)
    client.close()
    print(from_server)

    i = i+1
