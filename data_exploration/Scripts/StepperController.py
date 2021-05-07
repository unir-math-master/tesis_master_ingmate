#!/usr/bin/python3

import Jetson.GPIO as GPIO
import time

#Azimuth
#EnablePin = 11
#StepPin = 12
#DirectionPin = 13

#Elevation
EnablePin = 15
StepPin = 16
DirectionPin = 18

TimeSleep = 0.004
SetMode = GPIO.BOARD

channels = [EnablePin,StepPin,DirectionPin]
GPIO.setmode(SetMode)
GPIO.setwarnings(False)
GPIO.setup(channels, GPIO.OUT, initial=GPIO.LOW)

try:
    GPIO.output(EnablePin, GPIO.LOW)
    time.sleep(0.1)

    while True:
        GPIO.output(DirectionPin, GPIO.LOW)
        for i in range(0,1000):
            GPIO.output(StepPin, GPIO.HIGH)
            time.sleep(TimeSleep)
            GPIO.output(StepPin, GPIO.LOW)
            time.sleep(TimeSleep)
        time.sleep(3)

        GPIO.output(DirectionPin, GPIO.HIGH)
        for i in range(0,1000):
            GPIO.output(StepPin, GPIO.HIGH)
            time.sleep(TimeSleep)
            GPIO.output(StepPin, GPIO.LOW)
            time.sleep(TimeSleep)
        time.sleep(3)

except KeyboardInterrupt:
    GPIO.output(EnablePin, GPIO.HIGH)
    print("Saliendo del controlador de motor")

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    GPIO.cleanup()
    pass