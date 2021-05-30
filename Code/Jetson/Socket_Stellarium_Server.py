#!/usr/bin/python3

import socket, json, yaml

with open('Socket_Stellarium_Server_Parameters.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

#Constants
port = data['port']
ip = data['ip']

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((ip, port))

while True:
    socket.listen(5)
    client, address = socket.accept()
    #print("Connected to %s on port %s" % (address, port))

    response = client.recv(255)
    if response != "":
            stellarium_js = response.decode()
            stellarium_js = json.loads(stellarium_js)
            print(stellarium_js)

    st = "Recibido paquete: " + str(stellarium_js['index'])
    message = st.encode()        
    client.send(message)            

client.close()
stock.close()