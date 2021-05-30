#!/usr/bin/python3

import Jetson.GPIO as GPIO
from threading import Thread
import socket, json, yaml, threading, time

with open('Telescope_Server.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

#----------Constants----------
#Socket
port = data['port']
ip = data['ip']

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
Az_Reference_Angle = 120
El_Reference_Angle = 20
Az_Setpoint_Angle = 0
El_Setpoint_Angle = 0

class Sensors(Thread):
    pass

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

    def step(self, TS):
        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(TS)
        GPIO.output(self.step_pin, GPIO.LOW)
        time.sleep(TS)

    def run(self):
        print("%s DVR8825 Mode: %s" %(self.name,self.mode))
        GPIO.output(self.enable_pin, GPIO.LOW)
        print("Controlador de %s habilitado" %self.name)

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

    try:
        Azim_Process.start()
        Elev_Process.start()

        Azim_Process.reference(Az_Reference_Angle)
        Elev_Process.reference(El_Reference_Angle)

        while True:
            socket.listen(5)
            client, address = socket.accept()

            response = client.recv(255)
            if response != "":
                    stellarium_js = response.decode()
                    stellarium_js = json.loads(stellarium_js)

                    Az_Setpoint_Angle = stellarium_js['azimuth']
                    El_Setpoint_Angle = stellarium_js['altitude']

            st = "Recibido paquete: " + str(stellarium_js['index'])
            message = st.encode()        
            client.send(message)  

            Azim_Process.setpoint(Az_Setpoint_Angle)
            Elev_Process.setpoint(El_Setpoint_Angle)

            Azim_Process.main(TimeSleep)
            Elev_Process.main(TimeSleep)

    except KeyboardInterrupt:
        print("Saliendo del controlador de motor")

    except Exception as exception_error:
        print("Error: " + str(exception_error))
    
    finally:
        GPIO.cleanup()
        client.close()
        stock.close()