"""
Helper module that allows the use of the SenseHat LED matrix without needing to
rely on a bigger package. This also only requires wiring the SenseHat on the 
pins for power/ground and i2c instead of the entire array of pins
"""

import smbus

FRAMEBUFFER = [0x00] * 192
CTRL_ADDRESS = 0x46
I2CBUS = smbus.SMBus(1)

def clear():
    """
    Clears the matrix
    """
    for i in range(192):
        FRAMEBUFFER[i] = 0
        write_byte(i, 0)

def set_pixel(x, y, color):
    """
    Sets a pixel in the frame buffer. This does not set it on the actual LED
    matrix yet
    """
    FRAMEBUFFER[x * 24 + y] = color[0]
    FRAMEBUFFER[x * 24 + y + 8] = color[1]
    FRAMEBUFFER[x * 24 + y + 16] = color[2]

def flush_pixels():
    """
    Flushes any saved data from the frame buffer to the LED matrix
    """
    for i in range(192):
        I2CBUS.write_byte_data(CTRL_ADDRESS, i, FRAMEBUFFER[i])

def write_byte(addr, data):
    """
    Direct interaction with the i2c bus to write a specifc location
    """
    I2CBUS.write_byte_data(CTRL_ADDRESS, addr, data)
