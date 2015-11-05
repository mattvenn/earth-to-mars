import arduino
from arduino import Commands
from arduino import Arduino
from time import sleep

    
class ETMSensors():
    
    def __init__(self):
        self.board = Arduino()
        self.board.connect()

    def getH2(self):
        return int(self.board.sendCommand(Commands.READ_H2,0,0))

    def getTemp(self):
        return int(self.board.sendCommand(Commands.READ_TEMP,0,0)) / 10.0

    def getHumidity(self):
        return int(self.board.sendCommand(Commands.READ_HUMIDITY,0,0)) / 10.0

if __name__ == '__main__':
	e = ETMSensors()
	while True:
		print("h2=%d" % e.getH2())
		print("temp=%f" % e.getTemp())
		print("humidity=%f" % e.getHumidity())
		sleep(1)


