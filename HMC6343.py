#!usr/bin/python3

"""Python Library for HMC6343 on Raspberry Pi"""

import quick2wire.i2c as i2c
from time import sleep

__author__ = "Chethan Shettar"
__copyright__ = "Copyright 2016, Meuleman Electronics"
__credits__ = []
__license__ = ""
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = "c.shettar@meuleman.io"
__status__ = "Test"



class HMC6343(object):

##  HMC6343 I2C Address (0x32 >> 1 = 0x19)
    I2C_ADDR = 0x19

##  HMC6343 Registers
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

##  HMC6343 Commands
    POST_ACCEL = 0x40
    POST_MAG = 0x45
    POST_HEADING = 0x50
    POST_TILT = 0x55
    POST_OPMODE1 = 0x65
    ENTER_CAL = 0x71
    EXIT_CAL = 0x7E
    RESET = 0x82
    READ_EEPROM = 0xE1
    WRITE_EEPROM = 0xF1


##  HMC6343 Orientation Commands
    ORIENT_LEVEL = 0x72 ## X = forward, +Z = up (default)
    ORIENT_SIDEWAYS = 0x73 ## X = forward, +Y = up
    ORIENT_FLATFRONT = 0x74 ## Z = forward, -X = up

##  HMC6343 Setting Mode Commands
    ENTER_RUN = 0x75
    ENTER_STANDBY = 0x76
    ENTER_SLEEP = 0x83
    EXIT_SLEEP = 0x84

##  HMC6343 TIME DELAY IN SECONDS
    TD_PWR_UP = 0.5
    TD_RESET = 0.5
    TD_POST_DATA = 0.01
    TD_ENTER_MODE = 0.01
    TD_SET_ORIENTATION = 0.01
    TD_ENTER_SLEEP = 0.01
    TD_EXIT_SLEEP = 0.02
    TD_ENTER_CAL = 0.01
    TD_EXIT_CAL = 0.05
    TD_READ_EEPROM = 0.01
    TD_WRITE_EEPROM = 0.1
    TD_DEFAULT = 0.01

##  HMC6343 READ BYTE LENGTH
    BLEN_EEPROM_REG = 1
    BLEN_POST_DATA = 6

##  Constants
    MAX_16_BIT = 65535
    IIR_FILTER_ON = 0x20
    IIR_FILTER_OFF = 0xDF


    def __init__(self, mode=None, orientation=None):
        if(mode ==  None):
            self.selectMode(self.ENTER_RUN)
        else:
            self.selectMode(mode)

        if(orientation == None):
            self.setOrientation(self.ORIENT_LEVEL)
        else:
            self.setOrientation(orientation)
    


    def readEEPROM(self, reg):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.READ_EEPROM, reg))
            sleep(self.TD_READ_EEPROM)
            readValue = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_EEPROM_REG))
            print("Value at Reg %02x = %d" %(reg,readValue[0][0]))    
            print("Value at Reg %02x in hex = 0x%02x" %(reg,readValue[0][0]))    

    def writeEEPROM(self, reg, value):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.WRITE_EEPROM, reg, value))
            sleep(self.TD_WRITE_EEPROM)

            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.READ_EEPROM, reg))
            sleep(self.TD_READ_EEPROM)
            readValue = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_EEPROM_REG))

            if(readValue[0][0] == value):
                print("Reg 0x%02x written with 0x%02x successfully" %(reg, readValue[0][0]))
            else:
                print("Write not successful")

                
    def readFilterValue(self):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.READ_EEPROM, self.FILTER_LSB))
            sleep(self.TD_READ_EEPROM)
            filterL = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_EEPROM_REG))
            sleep(self.TD_DEFAULT)
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.READ_EEPROM, self.FILTER_MSB))
            sleep(self.TD_READ_EEPROM)
            filterM = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_EEPROM_REG))
            filterValue = (256*filterM[0][0] + filterL[0][0])
            print("Filter Value = %d" %filterValue) 


    def readAccel(self):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.POST_ACCEL))
            sleep(self.TD_POST_DATA)
            readValues = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_POST_DATA))
            
            accelX = (256*readValues[0][0] + readValues[0][1])
            if(accelX & 0x01<<15 != 0x00):
                accelX = (-(self.MAX_16_BIT+1) + accelX)        
            accelX = accelX/1024.0
            
            accelY = (256*readValues[0][2] + readValues[0][3])
            if(accelY & 0x01<<15 != 0x00):
                accelY = (-(self.MAX_16_BIT+1) + accelY)        
            accelY = accelY/1024.0
            
            accelZ = (256*readValues[0][4] + readValues[0][5])
            if(accelZ & 0x01<<15 != 0x00):
                accelZ = (-(self.MAX_16_BIT+1) + accelZ)        
            accelZ = accelZ/1024.0

            print("AccelX = %f" %accelX)
            print("AccelY = %f" %accelY)
            print("AccelZ = %f" %accelZ)

    def readMag(self):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.POST_MAG))
            sleep(self.TD_POST_DATA)
            readValues = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_POST_DATA))
            
            magX = (256*readValues[0][0] + readValues[0][1])
            if(magX & 0x01<<15 != 0x00):
                magX = (-(self.MAX_16_BIT+1) + magX)
            magX = magX/10.0
            
            magY = (256*readValues[0][2] + readValues[0][3])
            if(magY & 0x01<<15 != 0x00):
                magY = (-(self.MAX_16_BIT+1) + magY)
            magY = magY/10.0
            
            magZ = (256*readValues[0][4] + readValues[0][5])
            if(magZ & 0x01<<15 != 0x00):
                magZ = (-(self.MAX_16_BIT+1) + magZ)
            magZ = magZ/10.0

            print("MagX = %f" %magX)
            print("MagY = %f" %magY)
            print("MagZ = %f" %magZ)

    def readHeading(self):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.POST_HEADING))
            sleep(self.TD_POST_DATA)
            readValues = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_POST_DATA))
            
            heading = (256*readValues[0][0] + readValues[0][1])/10.0
            
            pitch = (256*readValues[0][2] + readValues[0][3])
            if(pitch & 0x01<<15 != 0x00):
                pitch = (-(self.MAX_16_BIT+1) + pitch)
            pitch = pitch/10.0
            
            roll = (256*readValues[0][4] + readValues[0][5])
            if(roll & 0x01<<15 != 0x00):
                roll = (-(self.MAX_16_BIT+1) + roll)
            roll = roll/10.0

            print("Heading = %f" %heading)
            return heading

    def readTilt(self):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.POST_TILT))
            sleep(self.TD_POST_DATA)
            readValues = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_POST_DATA))

            pitch = (256*readValues[0][0] + readValues[0][1])
            if(pitch & 0x01<<15 != 0x00):
                pitch = (-(self.MAX_16_BIT+1) + pitch)
            pitch = pitch/10.0    

            roll = (256*readValues[0][2] + readValues[0][3])
            if(roll & 0x01<<15 != 0x00):
                roll = (-(self.MAX_16_BIT+1) + roll)
            roll = roll/10.0

            temp = (256*readValues[0][4] + readValues[0][5])
            if(temp & 0x01<<15 != 0x00):
                temp = (-(self.MAX_16_BIT+1) + temp)
            temp = temp/10.0    

            print("Pitch = %f" %pitch)
            print("Roll = %f" %roll)
            print("Temperature = %f" %temp)

    def readTemp(self):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.POST_TILT))
            sleep(self.TD_POST_DATA)
            readValues = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_POST_DATA))

            temp = (256*readValues[0][4] + readValues[0][5])
            if(temp & 0x01<<15 != 0x00):
                temp = (-(self.MAX_16_BIT+1) + temp)
            temp = temp/10.0    

            print("Pitch = %f" %pitch)
            print("Roll = %f" %roll)
            print("Temperature = %f" %temp)

    def readOPMode1(self):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.POST_OPMODE1))
            sleep(self.TD_POST_DATA)
            readValues = bus.transaction(i2c.reading(self.I2C_ADDR, self.BLEN_EEPROM_REG))

            print("Value of OpMode1= 0x%02x" %readValues[0][0])
            return readValues[0][0]

    def setOrientation(self, orientation):
        sleep(self.TD_DEFAULT)
        successFlag = 1
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, orientation))
            sleep(self.TD_SET_ORIENTATION)

            OPMode1 = self.readOPMode1()

            if(orientation == self.ORIENT_LEVEL):
                if(OPMode1 & 0x01 == 0):
                    successFlag = 0
            elif(orientation == self.ORIENT_SIDEWAYS):
                if(OPMode1 & 0x02 == 0):
                    successFlag = 0        
            elif(orientation == self.ORIENT_FLATFRONT):
                if(OPMode1 & 0x04 == 0):
                    successFlag = 0        
            else:
                print("Orientation value not valid")

            if(successFlag == 0):
                print("Failed to set orientation")
            else:
                print("Orientation set successfully")        

    def enterSleep(self):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.ENTER_SLEEP))
            sleep(self.TD_ENTER_SLEEP)
            print("Entered sleep mode")

    def exitSleep(self):
        sleep(self.TD_DEFAULT)
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.EXIT_SLEEP))
            sleep(self.TD_EXIT_SLEEP)

            OPMode1 = self.readOPMode1()

            if(OPMode1 & 0x18 == 0):
                print("Failed to exit sleep mode")
            else:        
                print("Exited sleep mode")    


    def selectMode(self, mode):
        sleep(self.TD_DEFAULT)
        successFlag = 1
        if(mode == self.ENTER_SLEEP):
            enterSleep()
            return
        else:
            with i2c.I2CMaster() as bus:
                bus.transaction(i2c.writing_bytes(self.I2C_ADDR, mode))
                sleep(self.TD_ENTER_MODE)

                OPMode1 = self.readOPMode1()

                if(mode == self.ENTER_RUN):
                    if(OPMode1 & 0x10 == 0):
                        successFlag = 0
                elif(mode == self.ENTER_STANDBY):
                    if(OPMode1 & 0x08 == 0):
                        successFlag = 0          
                else:
                    print("Mode value not valid")

                if(successFlag == 0):
                    print("Failed to set mode")
                else:
                    print("Mode set successfully")            

    def filterMode(self, switchValue):  #valid values are IIR_FILTER_ON/IIR_FILTER_OFF
        sleep(self.TD_DEFAULT)
        OPMode1 = self.readOPMode1()

        if(switchValue == self.IIR_FILTER_ON):
            OPMode1 = OPMode1 | IIR_FILTER_ON
        elif(switchValue == self.IIR_FILTER_OFF):
            OPMode1 = OPMode1 & IIR_FILTER_OFF
        else:
            print("Not valid switch value")
            return

        print("OPMode1 = 0x%02x" %OPMode1)
        self.writeEEPROM(OP_MODE1, OPMode1)

        
    def calibrateSensor(self):
        sleep(self.TD_DEFAULT)
        print("Entering Calibration Mode")
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.ENTER_CAL))
            sleep(self.TD_ENTER_CAL)
            input("Press Enter to exit calibration mode")
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.EXIT_CAL))
            sleep(self.TD_EXIT_CAL)
            print("Exited Calibration Mode")

    def resetProc(self):
        sleep(self.TD_DEFAULT)
        print("Resetting the HMC6343 processor")
        with i2c.I2CMaster() as bus:
            bus.transaction(i2c.writing_bytes(self.I2C_ADDR, self.RESET))
            sleep(self.TD_RESET)
            print("HMC 6343 Processor Reset")

        
    def readAllReg(self):
        self.readEEPROM(self.SLAVE_ADDR)
        self.readEEPROM(self.SW_VERSION)
        self.readEEPROM(self.OP_MODE1)
        self.readEEPROM(self.OP_MODE2)
        self.readEEPROM(self.SN_LSB)
        self.readEEPROM(self.SN_MSB)
        self.readEEPROM(self.DATE_CODE_YY) 
        self.readEEPROM(self.DATE_CODE_WW) 
        self.readEEPROM(self.DEVIATION_LSB)
        self.readEEPROM(self.DEVIATION_MSB)
        self.readEEPROM(self.VARIATION_LSB)
        self.readEEPROM(self.VARIATION_MSB)
        self.readEEPROM(self.XOFFSET_LSB)
        self.readEEPROM(self.XOFFSET_MSB)
        self.readEEPROM(self.YOFFSET_LSB)
        self.readEEPROM(self.YOFFSET_MSB)
        self.readEEPROM(self.ZOFFSET_LSB)
        self.readEEPROM(self.ZOFFSET_MSB)
        self.readEEPROM(self.FILTER_LSB)
        self.readEEPROM(self.FILTER_MSB)

if __name__ == '__main__':

    from time import sleep

    compass = HMC6343()
    while True:
        compass.readHeading()
        sleep(5)

