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
import time

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


i2cBus = smbus.SMBus(1)

def confirmAddress():
	addressRead = i2cBus.read_byte_data(HMC6343_I2C_ADDR, SLAVE_ADDR)
	print addressRead
	if(addressRead == HMC6343_I2C_ADDR):
		print "Address confirmed"
	else:
		print "Address not confirmed"
		
		
confirmAddress()		
	
