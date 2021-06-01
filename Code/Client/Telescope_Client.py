#!/usr/bin/env python3

import socket, httplib2, urllib, json, yaml

with open('Telescope_Client.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

HOST = data['server_host']
PORT = data['server_port']

http = httplib2.Http()

Stlm = {    "above_horizon":'',
            "altitude":'',
            "altitude_geometric":'',
            "azimuth":'',
            "azimuth_geometric":'',
            "localized_name": '',
            "type":'',
            "index":'',
        }

i = 0

#Variables
satellite = data['satellite']

def Data_Streamming():
    content = http.request("http://%s:%s/api/objects/info?name=%s&format=%s"
        %(data['api_host'], str(data['api_port']), satellite, data['format']), method="GET")[1]
    get_data = content.decode()
    json_st = json.loads(get_data)

    Stlm['above_horizon'] = json_st['above-horizon']
    Stlm['altitude'] = json_st['altitude']
    Stlm['altitude_geometric'] = json_st['altitude-geometric']
    Stlm['azimuth'] = json_st['azimuth']
    Stlm['azimuth_geometric'] = json_st['azimuth-geometric']
    Stlm['localized_name'] = json_st['localized-name']
    Stlm['type'] = json_st['type']
    Stlm['index'] = i
    st = json.dumps(Stlm)

    return st

def Stellarium_Calibration(lat,lon,alt):
    body = {'id':data['id'],
            'latitude': lat,
            'longitude': lon,
            'altitude': alt,
            'name': data['name'],
            'country': data['country'],
            'planet': data['planet']
            }
    url = "http://localhost:8090/api/location/setlocationfields"
    content = http.request(url, method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'},
                       body=urllib.parse.urlencode(body))[1]
    return content

def Stellarium_Status():
    url = "http://localhost:8090/api/main/status"
    content = http.request(url, method="GET")[1]
    return content


try:
    print(Stellarium_Calibration('14.64072', '-90.51327', '1508'))
    print(Stellarium_Status())

    text1=''
    text2=''

    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        st = Data_Streamming()

        client.send(st.encode())
        from_server = client.recv(255)
        client.close()
        text1 = from_server.decode()

        if(text1!=text2):
            print(text1)
            text2=text1

        i = i+1

except KeyboardInterrupt:
    http.close()

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    pass