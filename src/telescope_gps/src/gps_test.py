from gps import GPSTelescope

SERIAL_PORT = "/dev/ttyUSB0"

def main():
    telescope_gps = GPSTelescope(SERIAL_PORT)

    while True:
        telescope_gps.get_gps_data()

main()