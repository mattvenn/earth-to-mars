import arduino
from arduino import Commands
from arduino import Arduino
from time import sleep
    
class Neopixel():
    
    def __init__(self):
        self.board = Arduino()
        self.board.connect()

    def reset(self):
        return self.board.sendCommand(Commands.RESET_NEO_PIXELS,0,0)

    def writePixel(self,pixel,r,g,b):
        return self.board.sendCommand(Commands.WRITE_NEO_PIXEL,0,pixel,r,g,b)
        
