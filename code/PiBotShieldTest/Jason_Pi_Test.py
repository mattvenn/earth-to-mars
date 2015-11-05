#//////////////////////////////////////////////////////////
#
#	Program to test the Rpi interface to the PiBot
#
#	modules tested: LEDS
#			Button
#			Servo
#			Stepper
#
#	jason welsby 10/2015
#	
#/////////////////////////////////////////////////////////


import RPi.GPIO as GPIO
from time import sleep
import time
from servo import Servo
import servo 
from stepper import Stepper
from motors import Motors
#This program use the board numerotation for GPIOs, so up left is 1 and down right is 40
RED_LED_GPIO = 26
GREEN_LED_GPIO = 29
BLUE_LED_GPIO = 31

SERVO_A_GPIO = 26 #GPIO number, not board number       servo #1 on pcb
SERVO_B_GPIO = 25 #GPIO number, not board number	servo #2 on pcb
SERVO_C_GPIO = 20 #GPIO number, not board number	servo #3 on pcb

STEPPER_GPIOS =[16,33,32,18]#[23,13,12,24] #[16,33,32,18]
BUTTON_GPIO = 36  # push button active high

def main():
    try:
        init()
        print '---- test begin ----'
      	testLEDs()
	#testButton()
       	#testServo()
        testStepper()
	testMotor()
    except KeyboardInterrupt:
        print 'Keyboard interrupt, exiting the test program'
    except Exception, e:
        print 'An error occured'
        print e
    finally:
        GPIO.cleanup()

def init():
    GPIO.setmode(GPIO.BOARD)
   
def testButton():
    print '=== BUTTON TEST ==='
    time.sleep(2)
    GPIO.setup(BUTTON_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    if GPIO.input(BUTTON_GPIO) ==True:
	print 'Button pressed'
	GPIO.setup(RED_LED_GPIO,GPIO.OUT)
   	GPIO.setup(GREEN_LED_GPIO,GPIO.OUT)
    	GPIO.setup(BLUE_LED_GPIO,GPIO.OUT)
     	GPIO.output(RED_LED_GPIO,True)
    	GPIO.output(GREEN_LED_GPIO,False)
    	GPIO.output(BLUE_LED_GPIO,True)
        time.sleep(2)
        GPIO.output(RED_LED_GPIO,False)
    	GPIO.output(GREEN_LED_GPIO,False)
    	GPIO.output(BLUE_LED_GPIO,False)

def testLEDs():
    print '=== LED Test ==='
    print 'to do: LED PINs to output'
    GPIO.setup(RED_LED_GPIO,GPIO.OUT)
    GPIO.setup(GREEN_LED_GPIO,GPIO.OUT)
    GPIO.setup(BLUE_LED_GPIO,GPIO.OUT)
    print 'to do: LEDs off'
    GPIO.output(RED_LED_GPIO,False)
    GPIO.output(GREEN_LED_GPIO,False)
    GPIO.output(BLUE_LED_GPIO,False)
    print 'to do: Blue LED on for 1 second'
    switchOnLED(BLUE_LED_GPIO,1)
    print 'to do: Green LED on for 1 second'
    switchOnLED(GREEN_LED_GPIO,1)
    print 'to do: Red LED on for 1 second'
    switchOnLED(RED_LED_GPIO,1)

def switchOnLED(LED, duration):
    GPIO.output(LED,True)
    time.sleep(1)
    GPIO.output(LED,False)

def testServo():
    print '=== Servo Test ==='
    print 'to do: servo Turn each 0.5 second'

    #GPIO.setup(38,GPIO.OUT)
   # GPIO.output(38,True)
    for servoPin in SERVO_A_GPIO, SERVO_B_GPIO, SERVO_C_GPIO:
        type = servo.SERVO_ANGLE
        #if servoPin == SERVO_B_GPIO:
         #   type = servo.SERVO_CONTINUOUS
        servoMotor = Servo(servoPin,type) #servoPin
        for i in range(0,11,1):
            print 0.1*i
    	    servoMotor.set_normalized(0.1*i)
    	    time.sleep(0.5)
        servoMotor.set_normalized(0.5)

def testStepper():
    print '=== Stepper Test ==='
    print 'to do: Stepper PINs to output'
    stepper = Stepper()
    stepper.turn(90,100)
    stepper.turnAsync(-90,100)
    while(not stepper.isMovementFinished()):
        time.sleep(0.02)
    #stepper.stop()

def testMotor():
    print '=== Motor Test ==='
    print 'to do: Motor Right and Left turn CW 0.5s CCW 0.5s'
    print "forward"
    move = Motors()
    sleep(0.2)
    print "Turn on Motor Driver"
    move.enable()
    move.forward(80)
    sleep(1)
    move.stop()
    sleep(0.1)

    print "backward"
    move.backward(80)
    sleep(1)
    move.stop()
    sleep(1)

    print "right motor direction 0"
    move.rightMotor(80,0)
    sleep(1)
    move.stop()
    sleep(0.1)

    print "right motor direction 1"
    move.rightMotor(80,1)
    sleep(1)
    move.stop()
    sleep(1)

    print "left motor direction 0"
    move.leftMotor(80,0)
    sleep(1)
    move.stop()

    print "left motor direction 1"
    move.leftMotor(80,1)
    sleep(1)
    move.stop()
    

if __name__ == '__main__':
    main()
