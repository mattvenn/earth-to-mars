from arduino import Commands, Arduino
from time import sleep
from motors import Motors

board = Arduino()
board.connect()
move = Motors()

# draw a square

while True:
	print("forward")
	move.forward(50)
	sleep(1)
	move.stop()

	sleep(1)

	# turn
	print("turn")
	move.leftMotor(50, 1)
	move.rightMotor(50, 0)
	sleep(1)
	move.stop()

	sleep(1)


