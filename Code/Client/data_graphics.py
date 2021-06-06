#!/usr/bin/python3

"""
#Datos de Azimuth (Eje Z HMC5883L)
SELECT value.medition, value.status_val FROM unir_ingmate.value WHERE value.axis LIKE 'AngleZ' AND value.id_sensor LIKE (
    SELECT sensor.id FROM unir_ingmate.sensor WHERE sensor.id_test LIKE 18 AND sensor.id_sensor_catalog LIKE (
        SELECT sensor_catalog.id FROM unir_ingmate.sensor_catalog WHERE sensor_catalog.code LIKE 'HMC5883L'));
#Datos de Elevacion (Eje Y MPU6050)
SELECT value.medition, value.status_val FROM unir_ingmate.value WHERE value.axis LIKE 'AngleY' AND value.id_sensor LIKE (
    SELECT sensor.id FROM unir_ingmate.sensor WHERE sensor.id_test LIKE 18 AND sensor.id_sensor_catalog LIKE (
        SELECT sensor_catalog.id FROM unir_ingmate.sensor_catalog WHERE sensor_catalog.code LIKE 'MPU6050'));

#Datos de Azimuth y elevacion (API REST Stellarium)
SELECT data.azimuth, data.elevation FROM unir_ingmate.data WHERE data.type LIKE 'real' AND data.id_api LIKE (
    SELECT api.id FROM unir_ingmate.api WHERE api.id_test LIKE 18 AND id_api_catalog LIKE (
        SELECT api_catalog.id FROM unir_ingmate.api_catalog WHERE api_catalog.name LIKE 'Stellarium'));
"""

import yaml, mysql.connector
import matplotlib.pyplot as plt
import numpy as np

with open('data_graphics.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

ingmate_bdd = mysql.connector.connect(
    user=data['user'], 
    password=data['password'], 
    host=data['host'], 
    port=data['db_port'],
    database=data['database']
    )
cursor = ingmate_bdd.cursor()


Elev_Api = []
Azim_Api = []
Elev_Sen = []
Azim_Sen = []

def MediaMovilOperation(ArrayDataOp,Position,WindowOp):
    Sum = 0
    for x in range(WindowOp):
        Sum = Sum + float(ArrayDataOp[Position-x])

    FilterData = Sum/float(WindowOp)
    return FilterData

def MediaMovilFilter(ArrayData,Window):
    FilterArray=[]
    for x in range(len(ArrayData)):
        if(x>=Window):#si ya paso el minimo del indice del arreglo, el valor del promedio es en base al ancho de la ventana
            FilterArray.insert(x,MediaMovilOperation(ArrayData,x,Window))
        else:#Si x es menor al indice del arreglo, el valor a dividir es x
            FilterArray.insert(x,MediaMovilOperation(ArrayData,x,x+1))

    return FilterArray


try:
    az_sensor_q = "SELECT value.medition, value.status_val FROM unir_ingmate.value WHERE value.status_val LIKE 'in_site' AND value.axis LIKE 'AngleZ' AND value.id_sensor LIKE (SELECT sensor.id FROM unir_ingmate.sensor WHERE sensor.id_test LIKE 18 AND sensor.id_sensor_catalog LIKE (SELECT sensor_catalog.id FROM unir_ingmate.sensor_catalog WHERE sensor_catalog.code LIKE 'HMC5883L'))"
    el_sensor_q = "SELECT value.medition, value.status_val FROM unir_ingmate.value WHERE value.status_val LIKE 'in_site' AND value.axis LIKE 'AngleY' AND value.id_sensor LIKE (SELECT sensor.id FROM unir_ingmate.sensor WHERE sensor.id_test LIKE 18 AND sensor.id_sensor_catalog LIKE (SELECT sensor_catalog.id FROM unir_ingmate.sensor_catalog WHERE sensor_catalog.code LIKE 'MPU6050'))"
    az_el_api_q = "SELECT data.azimuth, data.elevation FROM unir_ingmate.data WHERE data.type LIKE 'real' AND data.id_api LIKE (SELECT api.id FROM unir_ingmate.api WHERE api.id_test LIKE 18 AND id_api_catalog LIKE (SELECT api_catalog.id FROM unir_ingmate.api_catalog WHERE api_catalog.name LIKE 'Stellarium'))"
           
    cursor.execute(az_sensor_q)
    j=0
    for i in cursor:
        if(j%348==0):
            Azim_Sen.append(1.27*(float(i[0]) + 305))
            j=0
        j=j+1

    cursor.execute(el_sensor_q)
    j=0
    for i in cursor:
        if(j%348==0):
            Elev_Sen.append(-float(i[0]))
            j=0
        j=j+1

    cursor.execute(az_el_api_q)
    j=0
    for i in cursor:
        if(j%1000==0):
            Azim_Api.append(float(i[0]))
            Elev_Api.append(float(i[1]))
            j=0
        j=j+1

    fig, ax = plt.subplots()

    filt_Azim = MediaMovilFilter(Azim_Sen,100)
    filt_Elev = MediaMovilFilter(Elev_Sen,100)

    ax.plot(Azim_Api, Elev_Api, label="Datos Stellarium")
    #ax.plot(Azim_Sen, Elev_Sen, label="Datos sensados no filtrados")
    ax.plot(filt_Azim, filt_Elev, label="Datos sensados filtrados")

    ax.set(xlabel='Azimut', ylabel='Elevacion', title='Seguimiento de coordenadas celestes.')
    plt.legend()
    ax.grid()
    plt.show()

except KeyboardInterrupt:
    print("Saliendo...")

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    pass