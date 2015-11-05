import arduino
from arduino import Commands
from arduino import Arduino
from time import sleep

LEFT_MOTOR_MINUS = 6
LEFT_MOTOR_PLUS = 5
RIGHT_MOTOR_MINUS = 9
RIGHT_MOTOR_PLUS = 10
    
class Motors():
    def __init__(self):
        self.board = Arduino()
        self.board.connect()

    def enable(self): #arduino.A2
        self.board.sendCommand(Commands.WRITE_DIGITAL,2,1)
    
    def disable(self):
        self.board.sendCommand(Commands.WRITE_DIGITAL,2,0)

    def forward(self, speed):
        self.disable()
        command = self.speedToCommand(speed)
        self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_MINUS,0)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_MINUS,0)
        self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_PLUS,command)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_PLUS,command)
        #commands are set, enable the motors
        self.enable()

    def backward(self, speed):
        self.disable()
        command = self.speedToCommand(speed)
        self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_PLUS,0)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_PLUS,0)
        self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_MINUS,command)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_MINUS,command)
        #commands are set, enable the motors
        self.enable()



    def leftMotor(self, speed, direction):
        self.disable()
        command = self.speedToCommand(speed)
        if(direction==1):
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_MINUS,0)
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_PLUS,command)
        else:
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_PLUS,0)
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_MINUS,command)
        self.enable()
    
    def rightMotor(self, speed, direction):
        self.disable()
        command = self.speedToCommand(speed)
        if(direction==1):
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_MINUS,0)
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_PLUS,command)
        else:
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_PLUS,0)
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_MINUS,command)
        self.enable()

    def stop(self):
        self.disable()
        self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_MINUS,0)
        self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_MINUS,0)
        self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_PLUS,0)
        self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_PLUS,0)

    def speedToCommand(self,speed):
        #speed between 0-100
        command = int(speed * 2.55)
        if(command > 255):
            command = 255
        return command

#sleep(1)
#print board.sendCommand(Commands.READ_ULTRASOUND,17,19)
