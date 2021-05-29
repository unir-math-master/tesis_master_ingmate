#!/usr/bin/python3

import mysql.connector, yaml, time

with open('Database.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

ingmate_bdd = mysql.connector.connect(
    user=data['user'], 
    password=data['password'], 
    host=data['host'], 
    database=data['database']
    )
cursor = ingmate_bdd.cursor()

#Variables
#Configuracion inicial
satellite = "moon"
Api_REST = "Stellarium"
#GPS
pos_type = 'gps'
sat_number=12
Latitude = 14.123456
Longitude = -90.123456
Altitude = 10.1234
#Api REST
Azimuth_Api = 10.1628
Elevation_Api = 20.1628
Type_Api = 'real'
#Sensors
MPU6050_Dic = {
    'Acc_X':1.123,
    'Acc_Y':2.234,
    'Acc_Z':3.345,
    'Gyr_X':4.456,
    'Gyr_Y':5.567,
    'Gyr_Z':6.678,
    'Temp':12.45
}
HMC5883L_Dic = {
    'Ang_X':2.098,
    'Ang_Y':3.876,
    'Ang_Z':4.765
}

BMP180_Dic = {
    'Press': 6.4352,
    'Temp': 7.4657
}

Steps_Dic = {
    'Azimuth': 3454,
    'Elevation': 45423
}

#******************************************************************************
#Seeds catalogos

#Catalogo api REST
sql = "INSERT IGNORE INTO "+data['database']+".api_catalog VALUES(%s,%s,%s)"

val = ("NULL", "Stellarium", "http://stellarium.org/")
cursor.execute(sql,val)
val = ("", "NASA", "http://nasa.gob")
cursor.execute(sql,val)

#catalogo sensores
sql = "INSERT IGNORE INTO sensor_catalog VALUES(%s,%s,%s)"

val = ("NULL", "MPU6050", "Inertial sensor")
cursor.execute(sql,val)
val = ("NULL", "HMC5883L", "Magnetometer")
cursor.execute(sql,val)
val = ("NULL", "BMP180", "Barometer")
cursor.execute(sql,val)

ingmate_bdd.commit()
#******************************************************************************

#Inicio, una sola vez.
sql = "INSERT INTO "+data['database']+".test VALUES(%s,%s,%s,%s)"
val = ( "NULL", 
        data['telescope'],
        satellite,time.
        strftime('%Y-%m-%d %H:%M:%S')
    )
cursor.execute(sql,val)
ingmate_bdd.commit()
id_test = cursor.lastrowid

#Seleccionar ID Catalogos
cursor.execute("SELECT api_catalog.id FROM api_catalog WHERE name LIKE '%s'" % Api_REST)
id_api_catalog = cursor.fetchone()[0]

cursor.execute("SELECT sensor_catalog.code,sensor_catalog.id FROM sensor_catalog")
sensor_catalog = cursor.fetchall()

for i in range(0,len(sensor_catalog)):
    if sensor_catalog[i][0] == 'MPU6050':
        id_MPU6050 = sensor_catalog[i][1]
    elif sensor_catalog[i][0] == 'HMC5883L':
        id_HMC5883L = sensor_catalog[i][1]
    elif sensor_catalog[i][0] == 'BMP180':
        id_BMP180 = sensor_catalog[i][1]
#******************************************************************************

#Posicion, GPS.
sql = "INSERT INTO "+data['database']+".position VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
val = ( "NULL",
        str(id_test),
        pos_type,
        str(sat_number),
        str(Latitude),
        str(Longitude),
        str(Altitude),
        time.strftime('%Y-%m-%d %H:%M:%S')
    )
cursor.execute(sql,val)
ingmate_bdd.commit()

#******************************************************************************

#Api REST
sql = "INSERT INTO "+data['database']+".api VALUES(%s,%s,%s)"
val = ( "NULL", 
        str(id_test), 
        id_api_catalog
    )
cursor.execute(sql,val)
ingmate_bdd.commit()
id_api = cursor.lastrowid


#Data table Api REST
sql = "INSERT INTO "+data['database']+".data VALUES(%s,%s,%s,%s,%s,%s)"
val = ( "NULL", 
        str(id_api),
        str(Azimuth_Api),
        str(Elevation_Api),
        str(Type_Api),
        time.strftime('%Y-%m-%d %H:%M:%S')
    )
cursor.execute(sql,val)
ingmate_bdd.commit()

#******************************************************************************

#Sensors
#MPU6050
sql = "INSERT INTO "+data['database']+".sensor VALUES (%s,%s,%s)"

val = ( "NULL", str(id_test), str(id_MPU6050))
cursor.execute(sql,val)
id_MPU6050_sensor = cursor.lastrowid

val = ( "NULL", str(id_test), str(id_HMC5883L))
cursor.execute(sql,val)
id_HMC5883L_sensor = cursor.lastrowid

val = ( "NULL", str(id_test), str(id_BMP180))
cursor.execute(sql,val)
id_BMP180_sensor = cursor.lastrowid

ingmate_bdd.commit()


sql = "INSERT INTO "+data['database']+".value VALUES(%s,%s,%s,%s,%s)"
#Agregar datos MPU6050 a Value
for KeyAxis in MPU6050_Dic:
    val = ( "NULL", 
            str(id_MPU6050_sensor),
            KeyAxis,
            str(MPU6050_Dic[KeyAxis]),
            time.strftime('%Y-%m-%d %H:%M:%S')
        )
    cursor.execute(sql,val)

#Agregar datos HMC5883L a Value
for KeyAxis in HMC5883L_Dic:
    val = ( "NULL", 
            str(id_HMC5883L_sensor),
            KeyAxis,
            str(HMC5883L_Dic[KeyAxis]),
            time.strftime('%Y-%m-%d %H:%M:%S')
        )
    cursor.execute(sql,val)

#Agregar datos BMP180 a Value
for KeyAxis in BMP180_Dic:
    val = ( "NULL", 
            str(id_BMP180_sensor),
            KeyAxis,
            str(BMP180_Dic[KeyAxis]),
            time.strftime('%Y-%m-%d %H:%M:%S')
        )
    cursor.execute(sql,val)


ingmate_bdd.commit()

#******************************************************************************

#Steps

sql = "INSERT INTO "+data['database']+".steps VALUES(%s,%s,%s)"

val = ( "NULL", str(id_test), 'azimuth')
cursor.execute(sql,val)
id_steps_azimuth = cursor.lastrowid

val = ( "NULL", str(id_test), 'elevation')
cursor.execute(sql,val)
id_steps_elevation = cursor.lastrowid

ingmate_bdd.commit()


sql = "INSERT INTO "+data['database']+".number_of_steps VALUES(%s,%s,%s,%s)"
#Agregar datos a Azimuth steps
val = ( "NULL", 
        str(id_steps_azimuth),
        str(Steps_Dic['Azimuth']),
        time.strftime('%Y-%m-%d %H:%M:%S')
    )
cursor.execute(sql,val)

val = ( "NULL", 
        str(id_steps_elevation),
        str(Steps_Dic['Elevation']),
        time.strftime('%Y-%m-%d %H:%M:%S')
    )
cursor.execute(sql,val)

ingmate_bdd.commit()