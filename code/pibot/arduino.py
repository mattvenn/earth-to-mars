import RPi.GPIO as GPIO
GPIO.setwarnings(False)

import serial
from time import sleep

#Raspberry's pin that command the reset of the arduino
ARDUINO_RESET = 7

A0=500
A1=501
A2=502
A3=503
A4=504
A5=505

class Commands:             # call with:
    READ_DIGITAL = 0        # result = sendCommand(READ_DIGITAL, pinNumberToRead, 0)
    READ_ANALOG = 1         # result = sendCommand(READ_ANALOG, pinNumberToRead, 0)
    WRITE_DIGITAL = 2       # sendCommand(WRITE_DIGITAL, pinNumberToBeWritten, 1 or 0)
    WRITE_PWM = 3           # sendCommand(WRITE_PWM, pinNumberToBeWritten, value 0-255 )
    READ_ULTRASOUND = 4     # result = sendCommand(READ_ULTRASOUND, triggerPin, echoPin)
    READ_LEFT_ENCODER = 5   # result = sendCommand(READ_LEFT_ENCODER,0,0)
    READ_RIGHT_ENCODER = 6  # result = sendCommand(READ_RIGHT_ENCODER,0,0)
    WRITE_NEO_PIXEL = 7     # sendCommand(WRITE_NEO_PIXEL, pinNumber, pixelNumber 0-8, r,g,b 0-255)
    RESET_NEO_PIXELS = 8    # sendCommand(RESET_NEO_PIXELS, pinNumber, 0)
    READ_RFID = 9           # read rfid

class Arduino:
    connected = False
    port = None

    def reset(self):
        Arduino.connected=False
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(ARDUINO_RESET,GPIO.OUT)
        GPIO.output(ARDUINO_RESET,GPIO.HIGH)
        sleep(0.1)
        GPIO.output(ARDUINO_RESET,GPIO.LOW)
        sleep(0.1)
        GPIO.output(ARDUINO_RESET,GPIO.HIGH)
        sleep(0.5)

    def connect(self):
        if(Arduino.connected):
            return
        #reseting the arduino board
        self.reset()
        # open the serial port at 115200 baud with a read timeout of 2 seconds
        Arduino.port = serial.Serial('/dev/ttyS0', 115200, timeout=2)
        Arduino.port.flushInput()
        Arduino.port.flushOutput()
        Arduino.port.write("\n".encode())
        Arduino.port.readline()
        Arduino.connected = True
        print "connected"

    def sendCommand(self,command,pin,value,*otherArguments):
        message = "{0},{1},{2}".format(command,pin,value)
        for argument in otherArguments:
            message += ",{0}".format(argument)
        message += '\n'
        #print message
        Arduino.port.write(message.encode())
        result = Arduino.port.readline()
        Arduino.port.flushInput()
        sleep(0.005)
        return result
