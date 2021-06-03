#!/usr/bin/python3

import Jetson.GPIO as GPIO
import threading
import time

Azimuth_EnablePin = 11
Azimuth_StepPin = 12
Azimuth_DirectionPin = 13
Elevation_EnablePin = 15
Elevation_StepPin = 16
Elevation_DirectionPin = 18

TimeSleep = 0.001
SetMode = GPIO.BOARD

channels = [Azimuth_EnablePin,Azimuth_StepPin,Azimuth_DirectionPin,Elevation_EnablePin,Elevation_StepPin,Elevation_DirectionPin]
GPIO.setmode(SetMode)
GPIO.setwarnings(False)
GPIO.setup(channels, GPIO.OUT, initial=GPIO.HIGH)

dvr8825_mode = {'000':1, '100':1/2, '010':1/4, '110':1/8, '001':1/16, '101':1/32, '011':1/32, '111':1/32}

Az_Mode = '111'
El_Mode = '111'

In = 0

Az_Angle = 20
El_Angle = 45

try:
    GPIO.output(Elevation_EnablePin, GPIO.LOW)
    GPIO.output(Azimuth_EnablePin, GPIO.LOW)
    time.sleep(0.1)

    #Az_Angle = 1.8*Step*dvr8825_mode[mode]/27
    Nema_Az_Steps = int((Az_Angle*27)/(1.8*dvr8825_mode[Az_Mode]))
    Nema_El_Steps = int((El_Angle*27)/(1.8*dvr8825_mode[El_Mode]))


    GPIO.output(Azimuth_DirectionPin, GPIO.HIGH)
    Step = Azimuth_StepPin
    text = 'Azimuth +'
    
    #GPIO.output(Azimuth_DirectionPin, GPIO.LOW)
    #Step = Azimuth_StepPin
    #text = 'Azimuth -'

    for Az_counter in range(0,Nema_Az_Steps):
        GPIO.output(Step, GPIO.HIGH)
        time.sleep(TimeSleep)
        GPIO.output(Step, GPIO.LOW)
        time.sleep(TimeSleep)



    
    #GPIO.output(Elevation_DirectionPin, GPIO.HIGH)
    #Step = Elevation_StepPin
    #text = 'Elevation +'

    #GPIO.output(Elevation_DirectionPin, GPIO.LOW)
    #Step = Elevation_StepPin
    #text = 'Elevation -'

    #for Az_counter in range(0,Nema_El_Steps):
    #    GPIO.output(Step, GPIO.HIGH)
    #    time.sleep(TimeSleep)
    #    GPIO.output(Step, GPIO.LOW)
    #    time.sleep(TimeSleep)

except KeyboardInterrupt:
    GPIO.output(Elevation_EnablePin, GPIO.HIGH)
    print("Saliendo del controlador de motor")

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    GPIO.cleanup()
    pass
