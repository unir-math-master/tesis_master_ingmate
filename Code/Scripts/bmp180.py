#!/usr/bin/python
"""
Released under the MIT License
Copyright 2015-2016 MrTijn/Tijndagamer
"""

from bmp180 import bmp180

bmp = bmp180(0x77)

print("Temp: " + str(bmp.get_temp()) + " Celcius")
print("Pressure: " + str(bmp.get_pressure()) + " Pascal")
print("Altitude: " + str(bmp.get_altitude()) + " meter")