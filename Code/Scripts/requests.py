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
        content = http.request("http://localhost:8090/api/objects/info?name=moon&format=json")[1]
        get_data = content.decode()
        json_st = json.loads(get_data)

        Stlm['above_horizon'] = json_st['above-horizon']
        Stlm['altitude'] = json_st['altitude']
        Stlm['altitude_geometric'] = json_st['altitude-geometric']
        Stlm['azimuth'] = json_st['azimuth']
        Stlm['azimuth_geometric'] = json_st['azimuth-geometric']
        Stlm['type'] = json_st['type']
        Stlm['index'] = i

        print(Stlm)
        i=i+1

except KeyboardInterrupt:
    http.close()

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    pass