#!/usr/bin/python3

import time
import serial

GPS = { "Time":'',
        "Latitude":'',
        "Longitude":'',
        "Cardinal_Lat":'',
        "Cardinal_Lon":'',
        "Fix_Quality":'',
        "Satellites":'',
        "Horizontal_Dilution":'',
        "Altitude":'',
        "Measure_Altitude":'',
        "Geoid_Height":'',
        "Measure_Geoid":'',
        "Checksum":'',
        "Mode_1":'',
        "Mode_2":'',
        "IDs_SVs":'',
        "PDOP":'',
        "HDOP":'',
        "VDOP":'',
        "Time_of_fix":'',
        "Nav_warning":'',
        "Lat_Min_Notrh":'',
        "Lat_Min_North_Card":'',
        "Lat_Min_West":'',
        "Lat_Min_West_Card":'',
        "Speed_over_ground":'',
        "Course_made_good":'',
        "Date_of_fix":'',
        "Magnetic_Variation":'',
        "Magnetic_Variation_Card":'',
        "Mandatory_Checksum":'',
        "Track_made_good":'',
        "Track_made_good_relative":'',
        "Speed_over_ground_1":'',
        "Measure_speed_over_ground_1":'',
        "Speed_over_ground_2":'',
        "Measure_speed_over_ground_2":'',
        "Checksum_GPVTG":''
        }

SerialPort = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
time.sleep(1)

try:
    while True:
        if SerialPort.inWaiting() > 0:
            data = SerialPort.readline()
            data = data.decode("utf-8")
            data = data.replace('\r\n','')
            data = data.replace('$','')
            data = data.split(',')

            if(data[0]=='GPGGA'):
                #Global Positioning System Fix Data
                GPS['Time'] = data[1]
                GPS['Latitude'] = data[2]
                GPS['Cardinal_Lat'] = data[3]
                GPS['Longitude'] = data[4]
                GPS['Cardinal_Lon'] = data[5]
                GPS['Fix_Quality'] = data[6]
                GPS['Satellites'] = data[7]
                GPS['Horizontal_Dilution'] = data[8] 
                GPS['Altitude'] = data[9]
                GPS['Measure_Alt'] = data[10]
                GPS['Geoid_Height'] = data[11]
                GPS['Measure_Geoid'] = data[12]
                GPS['Checksum_GPGGA'] = data[14].replace('0000','')

            elif(data[0]=='GPGSA'):
                #GPS DOP and Active Satellites
                GPS['Mode_1'] = data[1]
                GPS['Mode_2'] = data[2]
                GPS['IDs_SVs'] = ''
                for i in range(3,15):
                    GPS['IDs_SVs'] = GPS['IDs_SVs'] + data[i] + ","
                GPS['PDOP'] = data[15]
                GPS['HDOP'] = data[16]
                GPS['VDOP'] = data[17]

            elif(data[0]=='GPGSV'):
                #GPS Satellites in view
                NumberOfMessages = data[1]
                #for i in range(0,int(NumberOfMessages)):
                #    print('Hola')
                MessageNumber = data[2]
                
                GPS['Number_of_SVs'] = data[3]
                GPS['SV_PRN_Number'] = data[4]
                GPS['Elevation'] = data[5]
                GPS['Azimuth'] = data[6]
                GPS['SNR'] = data[7]

            elif(data[0]=='GPRMC'):
                #GPS/Transit Data
                GPS['Time_of_fix'] = data[1]
                GPS['Nav_warning'] = data[2]
                GPS['Lat_Min_Notrh'] = data[3]
                GPS['Lat_Min_North_Card'] = data[4]
                GPS['Lat_Min_West'] = data[5]
                GPS['Lat_Min_West_Card'] = data[6]
                GPS['Speed_over_ground'] = data[7]
                GPS['Course_made_good'] = data[8]
                GPS['Date_of_fix'] = data[9]
                GPS['Magnetic_Variation'] = data[10]
                GPS['Magnetic_Variation_Card'] = data[11]
                GPS['Mandatory_Checksum'] = data[12]

            elif(data[0]=='GPVTG'):
                GPS['Track_made_good'] = data[1]
                GPS['Track_made_good_relative'] = data[2]
                GPS['Speed_over_ground_1'] = data[5]
                GPS['Measure_speed_over_ground_1'] = data[6]
                GPS['Speed_over_ground_2'] = data[7]
                GPS['Measure_speed_over_ground_2'] = data[8]
                GPS['Checksum_GPVTG'] = data[9]

            print(data)
        else:
            pass

except KeyboardInterrupt:
    print("Saliendo de lector de GPS")

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    SerialPort.close()
    pass