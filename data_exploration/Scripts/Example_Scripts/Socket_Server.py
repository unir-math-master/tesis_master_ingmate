#!/usr/bin/python3

import socket

port = 15556

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', port))

while True:
    socket.listen(5)
    client, address = socket.accept()
    print("Connected to %s on port %s" % (address, port))

    response = client.recv(255)
    if response != "":
            print(response)

    st = "Hola"
    message = st.encode()        
    client.send(message)            

client.close()
stock.close()