import smbus, math, argparse

bus = smbus.SMBus(1)

bus.write_byte_data(0x1E, 0x00, 0xF8)
bus.write_byte_data(0x1E, 0x01, 0xE0)
bus.write_byte_data(0x1E, 0x02, 0x00)

Declination = 0.67#0.67° E  ± 0.33°  changing by  0.12° W per year
#https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml

while True:
    data = bus.read_i2c_block_data(0x1E, 0x03, 6)

    xMag = data[0] * 256 + data[1]
    if xMag > 32767 :
        xMag -= 65536

    zMag = data[2] * 256 + data[3]
    if zMag > 32767 :
        zMag -= 65536

    yMag = data[4] * 256 + data[5]
    if yMag > 32767 :
        yMag -= 65536

    #print("X: %d" %xMag)
    #print("Y: %d" %yMag)
    #print("Z: %d" %zMag)

    Angle = math.atan2(yMag,xMag)
    Angle = math.degrees(Angle)
    Angle = Angle - Declination

    print(Angle)