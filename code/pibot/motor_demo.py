from arduino import Commands, Arduino
from time import sleep
from motors import Motors

board = Arduino()
board.connect()
move = Motors()

power = 100

# draw a square

while True:
	print("forward")
	move.forward(power)
	sleep(1)
	move.stop()

	sleep(1)

	# turn
	print("turn")
	move.leftMotor(power, 1)
	move.rightMotor(power, 0)
	sleep(1)
	move.stop()

	sleep(1)


