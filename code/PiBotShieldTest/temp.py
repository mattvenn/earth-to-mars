import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
while True:
    GPIO.setup(26,GPIO.OUT)
    GPIO.output(26,False)
