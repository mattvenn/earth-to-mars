from arduino import Commands
from arduino import Arduino
from ultrasound import Ultrasound
from time import sleep
from motors import Motors
from neopixel import Neopixel

board = Arduino()
board.connect()
sleep(2)
print "Switching arduino's PIN 13 ON"
board.sendCommand(Commands.WRITE_DIGITAL,13,1)
sleep(1)
print "Switching it OFF"
board.sendCommand(Commands.WRITE_DIGITAL,13,0)

print "Switching neopixels ON"
neopixels = Neopixel()
neopixels.reset()
for i in range(1,8):
    neopixels.writePixel(i,255,155,55)
    sleep(0.5)
neopixels.reset()

print "Reading Right Encoder Value"
print board.sendCommand(Commands.READ_RIGHT_ENCODER,0,0)

print "Getting ultrasound distance"
ultra = Ultrasound()
print ultra.getDistance()
print "Not working properly.... WTF is the distance and why 503?"

print "Now Testing the button"
#print "Button is at {0}".format(board.sendCommand(Commands.READ_DIGITAL,2,0))
#print "Push the button"
#while (not board.sendCommand(Commands.READ_DIGITAL,2,0).__contains__("1")):
#   sleep(0.05)
print "Button pressed!"
print "actually suicide button now connected to Pi!!!!"
sleep(1)
print "Turn on Motor Driver"
board.sendCommand(Commands.WRITE_DIGITAL,2,1)

print "Now testing Motors"
move = Motors()
sleep(0.2)

print "forward"
move.forward(50)
sleep(1)
move.stop()
sleep(0.1)

print "backward"
move.backward(50)
sleep(1)
move.stop()
sleep(1)

print "right motor direction 0"
move.rightMotor(50,0)
sleep(1)
move.stop()
sleep(0.1)

print "right motor direction 1"
move.rightMotor(50,1)
sleep(1)
move.stop()
sleep(1)

print "left motor direction 0"
move.leftMotor(50,0)
sleep(1)
move.stop()

print "left motor direction 1"
move.leftMotor(50,1)
sleep(1)
move.stop()
#sleep(1)
#print board.sendCommand(Commands.READ_ULTRASOUND,17,19)
