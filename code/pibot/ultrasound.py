import arduino
from arduino import Commands
from arduino import Arduino
from time import sleep

TRIGGER_PIN = arduino.A3
    
class Ultrasound():
    
    def __init__(self):
        self.board = Arduino()
        self.board.connect()

    def getDistance(self):
        return int(self.board.sendCommand(Commands.READ_ULTRASOUND,TRIGGER_PIN,0))

if __name__ == '__main__':
	ultra = Ultrasound()
	while True:
		print(ultra.getDistance())
		sleep(1)
