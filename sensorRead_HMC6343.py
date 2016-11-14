#!/usr/bin/env python

"""sensorRead_HMC6343.py: Reads the raw values and the sensor fusion data from the HMC6343 compass sensor"""

__author__ = "Chethan Shettar"
__copyright__ = "Copyright 2016, Meuleman Electronics"
__credits__ = []
__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = ""
__status__ = ""

import smbus
import smbus2
import time
import Adafruit_GPIO.I2C as I2C

## HMC6343 I2C Address (0x32 >> 1 = 0x19)
HMC6343_I2C_ADDR = 0x19

## HMC6343 Registers
SLAVE_ADDR = 0x00
SW_VERSION = 0x02
OP_MODE1 = 0x04
OP_MODE2 = 0x05
SN_LSB = 0x06
SN_MSB = 0x07
DATE_CODE_YY = 0x08 
DATE_CODE_WW = 0x09 
DEVIATION_LSB = 0x0A
DEVIATION_MSB = 0x0B
VARIATION_LSB = 0x0C
VARIATION_MSB = 0x0D
XOFFSET_LSB = 0x0E
XOFFSET_MSB = 0x0F
YOFFSET_LSB = 0x10
YOFFSET_MSB = 0x11
ZOFFSET_LSB = 0x12
ZOFFSET_MSB = 0x13
FILTER_LSB = 0x14
FILTER_MSB = 0x15

## HMC6343 Commands
POST_ACCEL = 0x40
POST_MAG = 0x45
POST_HEADING = 0x50
POST_TILT = 0x55
POST_OPMODE1 = 0x65
ENTER_CAL = 0x71
ORIENT_LEVEL = 0x72
ORIENT_SIDEWAYS = 0x73
ORIENT_FLATFRONT = 0x74
ENTER_RUN = 0x75
ENTER_STANDBY = 0x76
EXIT_CAL = 0x7E
RESET = 0x82
ENTER_SLEEP = 0x83
EXIT_SLEEP = 0x84
READ_EEPROM = 0xE1
WRITE_EEPROM = 0xF1

## HMC6343 Orientations
LEVEL = 0     ## X = forward, +Z = up (default)
SIDEWAYS = 1  ## X = forward, +Y = up
FLATFRONT = 2 ## Z = forward, -X = up
		
# I2C.require_repeated_start()

bus = smbus.SMBus(1)
bus2 = smbus2.SMBus(1)

defaultBusNum = I2C.get_default_bus()
deviceHMC6343 = I2C.get_i2c_device(HMC6343_I2C_ADDR, defaultBusNum)

# readAddress = deviceHMC6343.readU8(SLAVE_ADDR)
# readSwVer = deviceHMC6343.readU8(SW_VERSION)
# busRead = deviceHMC6343.readRaw8()
# readHeading = deviceHMC6343.readList(POST_HEADING, 6)

readAddress = bus.read_byte_data(HMC6343_I2C_ADDR, SLAVE_ADDR)
bus.close
print readAddress

readAddress = bus2.read_byte_data(HMC6343_I2C_ADDR, SLAVE_ADDR)
bus2.close
print readAddress



#readAddress = bus.read_block_data(HMC6343_I2C_ADDR, SLAVE_ADDR)
#print readAddress
#readAddress = bus.read_i2c_block_data(HMC6343_I2C_ADDR, SLAVE_ADDR)
#print readAddress


#readHeading = bus.read_i2c_block_data(HMC6343_I2C_ADDR, POST_HEADING)
#print readHeading
#heading = (readHeading[0]*256 + readHeading[1])/10.0
#print readHeading[0]
#print readHeading[1]
#print heading

#readAccel = bus.read_i2c_block_data(HMC6343_I2C_ADDR, POST_ACCEL)
#print readAccel
#accelX = (readHeading[0]*256 + readHeading[1])
#print readHeading[0]
#print readHeading[1]
#print accelX
	
