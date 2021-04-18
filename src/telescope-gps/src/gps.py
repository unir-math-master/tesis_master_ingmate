#!/usr/bin/env python3

import time
import board
import busio
import serial
import adafruit_gps

SERIAL_PORT = "/dev/ttyUSB0"

class GPSTelescope:
    def __init__(self, serial_port="/dev/ttyUSB0"):
        self.uart = serial.Serial(serial_port, baudrate=9600, timeout=10)
        self.gps = adafruit_gps.GPS(self.uart, debug=False)
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        self.gps.send_command(b"PMTK220,1000")

    def get_gps_data(self):
        last_print = time.monotonic()
        while True:
            self.gps.update()
            # Every second print out current location details if there's a fix.
            current = time.monotonic()
            if current - last_print >= 1.0:
                last_print = current
                if not self.gps.has_fix:
                    # Try again if we don't have a fix yet.
                    print("Waiting for fix...")
                    continue
                # We have a fix! (gps.has_fix is true)
                # Print out details about the fix like location, date, etc.
                print("=" * 40)  # Print a separator line.
                print(
                    "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                        self.gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                        self.gps.timestamp_utc.tm_mday,  # struct_time object that holds
                        self.gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                        self.gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                        self.gps.timestamp_utc.tm_min,  # month!
                        self.gps.timestamp_utc.tm_sec,
                    )
                )
                print("Latitude: {0:.6f} degrees".format(self.gps.latitude))
                print("Longitude: {0:.6f} degrees".format(self.gps.longitude))
                print("Fix quality: {}".format(self.gps.fix_quality))
                # Some attributes beyond latitude, longitude and timestamp are optional
                # and might not be present.  Check if they're None before trying to use!
                if self.gps.satellites is not None:
                    print("# satellites: {}".format(self.gps.satellites))
                if self.gps.altitude_m is not None:
                    print("Altitude: {} meters".format(self.gps.altitude_m))
                if self.gps.speed_knots is not None:
                    print("Speed: {} knots".format(self.gps.speed_knots))
                if self.gps.track_angle_deg is not None:
                    print("Track angle: {} degrees".format(self.gps.track_angle_deg))
                if self.gps.horizontal_dilution is not None:
                    print("Horizontal dilution: {}".format(self.gps.horizontal_dilution))
                if self.gps.height_geoid is not None:
                    print("Height geo ID: {} meters".format(self.gps.height_geoid))

