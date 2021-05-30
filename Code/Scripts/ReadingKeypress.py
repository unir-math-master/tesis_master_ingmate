#!/usr/bin/python3

import Jetson.GPIO as GPIO
import time

Azimuth_EnablePin = 11
Azimuth_StepPin = 12
Azimuth_DirectionPin = 13
Elevation_EnablePin = 15
Elevation_StepPin = 16
Elevation_DirectionPin = 18

TimeSleep = 0.05
SetMode = GPIO.BOARD

text = ''
n = 1

channels = [Azimuth_EnablePin,Azimuth_StepPin,Azimuth_DirectionPin,Elevation_EnablePin,Elevation_StepPin,Elevation_DirectionPin]
GPIO.setmode(SetMode)
GPIO.setwarnings(False)
GPIO.setup(channels, GPIO.OUT, initial=GPIO.HIGH)

try:
    GPIO.output(Elevation_EnablePin, GPIO.LOW)
    GPIO.output(Azimuth_EnablePin, GPIO.LOW)
    time.sleep(0.1)
    while True:
        c = input()

        if(c=='w'):
            GPIO.output(Elevation_DirectionPin, GPIO.HIGH)
            Step = Elevation_StepPin
            text = 'Elevation +'
        elif(c=='s'):
            GPIO.output(Elevation_DirectionPin, GPIO.LOW)
            Step = Elevation_StepPin
            text = 'Elevation -'
        elif(c=='d'):
            GPIO.output(Azimuth_DirectionPin, GPIO.HIGH)
            Step = Azimuth_StepPin
            text = 'Azimuth +'
        elif(c=='a'):
            GPIO.output(Azimuth_DirectionPin, GPIO.LOW)
            Step = Azimuth_StepPin
            text = 'Azimuth -'
        elif(c=='1'):
            n = 1
        elif(c=='2'):
            n = 10
        elif(c=='3'):
            n = 100

        if(c=='a' or c=='d' or c=='s' or c=='w'):
            for i in range(0,n):
                GPIO.output(Step, GPIO.HIGH)
                time.sleep(TimeSleep)
                GPIO.output(Step, GPIO.LOW)
                time.sleep(TimeSleep)

                print(text)
                print(n)

except KeyboardInterrupt:
    GPIO.output(Elevation_EnablePin, GPIO.HIGH)
    print("Saliendo del controlador de motor")

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    GPIO.cleanup()
    pass

