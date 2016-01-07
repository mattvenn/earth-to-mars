import arduino
from arduino import Commands
from arduino import Arduino
from time import sleep

    
class ETM():
    
    def __init__(self):
        self.board = Arduino()
        self.board.connect()

    def getRFID(self):
        return self.board.sendCommand(Commands.READ_RFID,0,0)

if __name__ == '__main__':
	e = ETM()
	while True:
		rfid = e.getRFID()
		rfid = rfid.strip()
		if len(rfid) == 12:
			print("rfid=%s" % rfid)
		sleep(0.1)


