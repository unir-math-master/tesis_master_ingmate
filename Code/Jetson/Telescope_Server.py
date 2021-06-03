#!/usr/bin/python3

import smbus, socket, json, yaml, threading, time, math, mysql.connector
import Jetson.GPIO as GPIO
from threading import Thread
from bmp180 import bmp180
from mpu6050 import mpu6050

with open('Telescope.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
#----------Constants----------
#Socket
port = data['sk_port']
ip = data['ip']

#Database Inicialization
ingmate_bdd = mysql.connector.connect(
    user=data['user'], 
    password=data['password'], 
    host=data['host'], 
    port=data['db_port'],
    database=data['database']
    )
cursor = ingmate_bdd.cursor()

ingmate_bdd_value = mysql.connector.connect(
    user=data['user'], 
    password=data['password'], 
    host=data['host'], 
    port=data['db_port'],
    database=data['database']
    )
cursor_value = ingmate_bdd_value.cursor()

#Motors movement
Azim_EnablePin = data['Azim_EnablePin']
Azim_StepPin = data['Azim_StepPin']
Azim_DirectionPin = data['Azim_DirectionPin']
Elev_EnablePin = data['Elev_EnablePin']
Elev_StepPin = data['Elev_StepPin']
Elev_DirectionPin = data['Elev_DirectionPin']

Coord_1 = data['Coordinate_1']
Coord_2 = data['Coordinate_2']
Az_Mode = data['Azimuth_Mode']
El_Mode = data['Elevation_Mode']

#Socket init
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((ip, port))

#GPIO init
SetMode = GPIO.BOARD
channels = [Azim_EnablePin,Azim_StepPin,Azim_DirectionPin,Elev_EnablePin,Elev_StepPin,Elev_DirectionPin]
GPIO.setmode(SetMode)
GPIO.setwarnings(False)
GPIO.setup(channels, GPIO.OUT, initial=GPIO.HIGH)

#DVR8825 Hardware configuration modes
dvr8825_mode = {'000':1, '100':1/2, '010':1/4, '110':1/8, '001':1/16, '101':1/32, '011':1/32, '111':1/32}

#Variables
TimeSleep = 0.001
Above_Horizon = False

Az_Reference_Angle = 180
El_Reference_Angle = 0
Az_Setpoint_Angle = 0
El_Setpoint_Angle = 0

satellite = data['satellite']
Api_REST = data['Api_REST']

status_val = "in_transit"

class Database():
    def __init__(self):
        self.id_test = 0
        self.id_api_catalog = 0
        self.id_api = 0

        self.id_MPU6050 = 0
        self.id_HMC5883L = 0
        self.id_BMP180 = 0
        self.id_MPU6050_sensor = 0
        self.id_HMC5883L_sensor = 0
        self.id_BMP180_sensor = 0

        self.id_steps_azimuth = 0
        self.id_steps_elevation = 0

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
        self.test()
        self.api()
        self.sensor()
        self.steps()

    def test(self):
        #Ingreso una unica vez
        sql = "INSERT INTO "+data['database']+".test VALUES(%s,%s,%s,%s)"
        val = ( "NULL", 
                data['telescope'],
                satellite,
                time.strftime('%Y-%m-%d %H:%M:%S')
            )
        cursor.execute(sql,val)
        ingmate_bdd.commit()
        self.id_test = cursor.lastrowid

        print("Test No. %s" %self.id_test) 

        #Seleccionar ID Catalogos
        cursor.execute("SELECT api_catalog.id FROM api_catalog WHERE name LIKE '%s'" % Api_REST)
        self.id_api_catalog = cursor.fetchone()[0]

        cursor.execute("SELECT sensor_catalog.code,sensor_catalog.id FROM sensor_catalog")
        sensor_catalog = cursor.fetchall()

        for i in range(0,len(sensor_catalog)):
            if sensor_catalog[i][0] == 'MPU6050':
                self.id_MPU6050 = sensor_catalog[i][1]
            elif sensor_catalog[i][0] == 'HMC5883L':
                self.id_HMC5883L = sensor_catalog[i][1]
            elif sensor_catalog[i][0] == 'BMP180':
                self.id_BMP180 = sensor_catalog[i][1]

    def position(self,pos_type,sat_number,latitude,longitude,altitude):
        sql = "INSERT INTO "+data['database']+".position VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        val = ( "NULL",
                str(self.id_test),
                pos_type,
                str(sat_number),
                str(latitude),
                str(longitude),
                str(altitude),
                time.strftime('%Y-%m-%d %H:%M:%S')
            )
        cursor.execute(sql,val)
        ingmate_bdd.commit()

    def api(self):
        sql = "INSERT INTO "+data['database']+".api VALUES(%s,%s,%s)"
        val = ( "NULL", 
                str(self.id_test), 
                self.id_api_catalog
            )
        cursor.execute(sql,val)
        ingmate_bdd.commit()
        self.id_api = cursor.lastrowid

    def data(self,azm,elv,tp_api):
        sql = "INSERT INTO "+data['database']+".data VALUES(%s,%s,%s,%s,%s,%s)"
        val = ( "NULL", 
                str(self.id_api),
                str(round(azm,15)),
                str(round(elv,15)),
                str(tp_api),
                time.strftime('%Y-%m-%d %H:%M:%S')
            )
        cursor.execute(sql, val)
        ingmate_bdd.commit()

    def sensor(self):
        sql = "INSERT INTO "+data['database']+".sensor VALUES (%s,%s,%s)"

        val = ( "NULL", str(self.id_test), str(self.id_MPU6050))
        cursor.execute(sql,val)
        self.id_MPU6050_sensor = cursor.lastrowid

        val = ( "NULL", str(self.id_test), str(self.id_HMC5883L))
        cursor.execute(sql,val)
        self.id_HMC5883L_sensor = cursor.lastrowid

        val = ( "NULL", str(self.id_test), str(self.id_BMP180))
        cursor.execute(sql,val)
        self.id_BMP180_sensor = cursor.lastrowid

        ingmate_bdd.commit()

    def steps(self):
        sql = "INSERT INTO "+data['database']+".steps VALUES(%s,%s,%s)"

        val = ( "NULL", str(self.id_test), 'azimuth')
        cursor.execute(sql,val)
        self.id_steps_azimuth = cursor.lastrowid

        val = ( "NULL", str(self.id_test), 'elevation')
        cursor.execute(sql,val)
        self.id_steps_elevation = cursor.lastrowid

        ingmate_bdd.commit()

    def number_of_steps(self,Type_St,St):
        pass

class Database_value():
    def __init__(self, id_MPU6050_sensor, id_HMC5883L_sensor, id_BMP180_sensor):
        self.id_MPU6050_sensor = id_MPU6050_sensor
        self.id_HMC5883L_sensor = id_HMC5883L_sensor
        self.id_BMP180_sensor = id_BMP180_sensor

    def value(self,MPU6050_Dic,HMC5883L_Dic,BMP180_Dic, Status_val): 
        sql = "INSERT INTO "+data['database']+".value VALUES(%s,%s,%s,%s,%s,%s)"

        for KeyAxis in MPU6050_Dic:
            val = ( "NULL", 
                    str(self.id_MPU6050_sensor),
                    KeyAxis,
                    str(MPU6050_Dic[KeyAxis]),
                    Status_val,
                    time.strftime('%Y-%m-%d %H:%M:%S')
                )
            cursor_value.execute(sql,val)

        for KeyAxis in HMC5883L_Dic:
            val = ( "NULL", 
                    str(self.id_HMC5883L_sensor),
                    KeyAxis,
                    str(HMC5883L_Dic[KeyAxis]),
                    Status_val,
                    time.strftime('%Y-%m-%d %H:%M:%S')
                )
            cursor_value.execute(sql,val)

        for KeyAxis in BMP180_Dic:
            val = ( "NULL", 
                    str(self.id_BMP180_sensor),
                    KeyAxis,
                    str(BMP180_Dic[KeyAxis]),
                    Status_val,
                    time.strftime('%Y-%m-%d %H:%M:%S')
                )
            cursor_value.execute(sql,val)

        ingmate_bdd_value.commit()

class Sensors(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.bmp180_dir = 0x77
        self.hmc5883l_dir = 0x1E
        self.mpu6050_dir = 0x68

        self.Accel_Range = 16384
        self.Gyro_Range = 131

        self.Angle1 = 0
        self.Angle2 = 0        

        #Database
        self.MPU6050_Dic = {
            'AngleX': 0,
            'AngleY': 0,
        }
        self.HMC5883L_Dic = {
            'AngleZ':0,
        }

        self.BMP180_Dic = {
            'Alt': 0,
        }

    def run(self):
        global status_val

        #inicializando bmp180
        print("Inicializando BMP180")
        self.bmp = bmp180(self.bmp180_dir)

        #inicializando mpu6050
        print("Inicializando MPU6050")
        self.mpu = mpu6050(self.mpu6050_dir)
        self.mpu.set_accel_range(0x00)
        self.mpu.set_gyro_range(0x00)

        #Inicializando ByPass de mpu6050 XDA yXCL para canal i2C de hmc5883L
        print("Inicializando Bypass XDA y XCL de canal I2C")
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.mpu6050_dir, 0x37, 0x02)
        self.bus.write_byte_data(self.mpu6050_dir, 0x6A, 0x00)

        #inicializando hmc5883l
        print("Inicializando HMC5883L")
        self.hmc = smbus.SMBus(1)
        self.hmc.write_byte_data(self.hmc5883l_dir, 0x00, 0xF8)
        self.hmc.write_byte_data(self.hmc5883l_dir, 0x01, 0xE0)
        self.hmc.write_byte_data(self.hmc5883l_dir, 0x02, 0x00)

        self.Declination = 0.67#0.67° E  ± 0.33°  changing by  0.12° W per year
        #https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml


        print("Sensores inicializados.")

        try:
            while True:
                self.BMP180_Dic['Alt'] = self.BMP180()
                self.MPU6050_Dic['AngleX'], self.MPU6050_Dic['AngleY'] = self.MPU6050()
                self.HMC5883L_Dic['AngleZ'] = self.HMC5883L()

                DataB_V.value(self.MPU6050_Dic,self.HMC5883L_Dic,self.BMP180_Dic,status_val)
        except KeyboardInterrupt:
            print("Saliendo de rutina de sensores")

    def GPS(self):
        pass

    def BMP180(self):
        temp = self.bmp.get_temp()
        pascal = self.bmp.get_pressure()
        meters = self.bmp.get_altitude()
        return meters

    def MPU6050(self):
        accel_data = self.mpu.get_accel_data()
        gyro_data = self.mpu.get_gyro_data()
        temp = self.mpu.get_temp()

        ax = accel_data['x']
        ay = accel_data['y']
        az = accel_data['z']
        gx = gyro_data['x']
        gy = gyro_data['y']
        gz = gyro_data['z']
        tm = temp

        Accel1 = math.degrees(math.atan( -1 * (float(ax) / self.Accel_Range) / math.sqrt(math.pow( (float(ay) / self.Accel_Range), 2) + math.pow( (float(az) / self.Accel_Range), 2))))
        Accel2 = math.degrees(math.atan(      (float(ay) / self.Accel_Range) / math.sqrt(math.pow( (float(ax) / self.Accel_Range), 2) + math.pow( (float(az) / self.Accel_Range), 2))))
        Gyro1 = float(gx) / self.Gyro_Range
        Gyro2 = float(gy) / self.Gyro_Range
        self.Angle1 = 0.99*(self.Angle1 + Gyro1*0.0010) + 0.01*Accel2
        self.Angle2 = 0.99*(self.Angle2 + Gyro2*0.0010) + 0.01*Accel1

        return self.Angle1, self.Angle2

    def HMC5883L(self):
        data = self.hmc.read_i2c_block_data(self.hmc5883l_dir, 0x03, 6)
        xMag = data[0] * 256 + data[1]
        if xMag > 32767 :
            xMag -= 65536
        zMag = data[2] * 256 + data[3]
        if zMag > 32767 :
            zMag -= 65536
        yMag = data[4] * 256 + data[5]
        if yMag > 32767 :
            yMag -= 65536

        Angle = math.atan2(yMag,xMag)
        Angle = math.degrees(Angle)
        Angle = Angle - self.Declination

        return Angle

class Coordinates(Thread):
    def __init__(self, name, mode, dir_pin, step_pin, enable_pin):
        Thread.__init__(self)
        self.name = name
        self.mode = mode
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.enable_pin = enable_pin
        self.Nema_Steps = 0
        self.Nema_Setpoint_Steps = 0
        self.status_val = 'in_transit'

    def run(self):
        print("%s DVR8825 Mode: %s" %(self.name,self.mode))
        GPIO.output(self.enable_pin, GPIO.LOW)
        print("Controlador de %s habilitado" %self.name)

    def step(self, TS):
        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(TS)
        GPIO.output(self.step_pin, GPIO.LOW)
        time.sleep(TS)

    def angle_to_steps(self, angle):
        return int((angle*27)/(1.8*dvr8825_mode[self.mode]))

    def reference(self, reference):
        self.Nema_Steps = self.angle_to_steps(reference)

    def setpoint(self, setpoint):
        self.Nema_Setpoint_Steps = self.angle_to_steps(setpoint)

    def feedback(self):
        pass

    def main(self, TS):
        if(self.Nema_Steps>self.Nema_Setpoint_Steps):
            GPIO.output(self.dir_pin, GPIO.LOW)
            self.step(TS)
            self.Nema_Steps = self.Nema_Steps - 1

        elif(self.Nema_Steps<self.Nema_Setpoint_Steps):
            GPIO.output(self.dir_pin, GPIO.HIGH)
            self.step(TS)
            self.Nema_Steps = self.Nema_Steps + 1

        elif(self.Nema_Steps==self.Nema_Setpoint_Steps):
            #print("objetivo centrado")
            self.status_val = "in_site"
            pass
        print(self.name + ", setpoint: " + str(self.Nema_Setpoint_Steps)+", var: "+str(self.Nema_Steps))

if __name__ == '__main__':
    Azim_Process = Coordinates(Coord_1, Az_Mode, Azim_DirectionPin, Azim_StepPin, Azim_EnablePin)
    Elev_Process = Coordinates(Coord_2, El_Mode, Elev_DirectionPin, Elev_StepPin, Elev_EnablePin)
    Sensors_Process = Sensors()

#    try: 
    DataB = Database()
    DataB_V = Database_value(DataB.id_MPU6050_sensor, DataB.id_HMC5883L_sensor, DataB.id_BMP180_sensor)
    time.sleep(0.5)

    Azim_Process.start()
    Elev_Process.start()
    Sensors_Process.start()

    Azim_Process.reference(Az_Reference_Angle)
    Elev_Process.reference(El_Reference_Angle)

    while True:
        socket.listen(5)
        client, address = socket.accept()

        response = client.recv(255)
        if response != "":
            stellarium_js = response.decode()
            stellarium_js = json.loads(stellarium_js)

            Above_Horizon = stellarium_js['above_horizon']
            Az_Setpoint_Angle = stellarium_js['azimuth']
            El_Setpoint_Angle = stellarium_js['altitude']

            DataB.data(Az_Setpoint_Angle,El_Setpoint_Angle,'real')
            print(status_val)
        #Movimiento de telescopio
        if(Above_Horizon!=False):
            Azim_Process.setpoint(Az_Setpoint_Angle)
            Elev_Process.setpoint(El_Setpoint_Angle)

            Azim_Process.main(TimeSleep)
            Elev_Process.main(TimeSleep)

            if(Azim_Process.status_val=='in_site' and Elev_Process.status_val=='in_site'):
                status_val = 'in_site'

            text = str(stellarium_js['localized_name'] +"->"+ stellarium_js['type'])
        else:
            text = "No es posible visualizar " + str(stellarium_js['localized_name']) + ", se encuentra debajo del horizonte."
            #print(text)

        st = "Recibiendo paquetes, " + text
        message = st.encode()        
        client.send(message)  

#    except KeyboardInterrupt:
#        print("Saliendo del controlador de motor")

#    except Exception as exception_error:
#        print("Error: " + str(exception_error))
    
#    finally:
#        GPIO.cleanup()
#        client.close()
#        socket.close()