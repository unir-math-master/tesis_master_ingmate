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

Az_Reference_Angle = 120
El_Reference_Angle = 20
Az_Setpoint_Angle = 0
El_Setpoint_Angle = 0

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
        MPU6050_Dic = {
            'AngleX': 0,
            'AngleY': 0,
        }
        HMC5883L_Dic = {
            'AngleZ':0,
        }

        BMP180_Dic = {
            'Alt': 0,
        }

    def run(self):
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
                altitude_bmp180 = self.BMP180()
                angleX_mpu6050, angleY_mpu6050 = self.MPU6050()
                angleZ_hmc5883l = self.HMC5883L()
                print(angle_mpu6050) 
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
            pass

        print(self.name + ", setpoint: " + str(self.Nema_Setpoint_Steps)+", var: "+str(self.Nema_Steps))

if __name__ == '__main__':
    Azim_Process = Coordinates(Coord_1, Az_Mode, Azim_DirectionPin, Azim_StepPin, Azim_EnablePin)
    Elev_Process = Coordinates(Coord_2, El_Mode, Elev_DirectionPin, Elev_StepPin, Elev_EnablePin)
    Sensors_Process = Sensors()

    try:
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

            #Movimiento de telescopio
            if(Above_Horizon!=False):
                Azim_Process.setpoint(Az_Setpoint_Angle)
                Elev_Process.setpoint(El_Setpoint_Angle)

                Azim_Process.main(TimeSleep)
                Elev_Process.main(TimeSleep)

                text = str(stellarium_js['localized_name'] +"->"+ stellarium_js['type'])
            else:
                text = "No es posible visualizar " + str(stellarium_js['localized_name']) + ", se encuentra debajo del horizonte."

            st = "Recibiendo paquetes, " + text
            message = st.encode()        
            client.send(message)  

    except KeyboardInterrupt:
        print("Saliendo del controlador de motor")

    except Exception as exception_error:
        print("Error: " + str(exception_error))
    
    finally:
        GPIO.cleanup()
        client.close()
        stock.close()