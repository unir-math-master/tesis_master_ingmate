#!/usr/bin/python3
 
import httplib2
import json
 
http = httplib2.Http()

Stlm = { "above_horizon":'',
                    "altitude":'',
                    "altitude_geometric":'',
                    "azimuth":'',
                    "azimuth_geometric":'',
                    "type":'',
                    "index":'',
                    }
i=0

try:
    while True:
        content = http.request("http://192.168.0.7:8090/api/objects/info?name=moon&format=json")[1]
        get_data = content.decode()
        json_st = json.loads(get_data)

        print(json_st)

except KeyboardInterrupt:
    exit()

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    pass