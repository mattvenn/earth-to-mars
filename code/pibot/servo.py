import os
import time

#SERVOD_PATH='/home/pi/ServoBlaster1/user/servod'
#SERVOD_PATH='/usr/local/sbin/servod'
SERVOD_PATH='/usr/sbin/pi-blaster'
SERVO_ANGLE = 0
SERVO_CONTINUOUS = 1

class Servo(object):
    """A Servo instance controls a single servo

    Parameters
    ----------
    pin : int
        GPIO pin number the servo is connected to
    type : int
        The kind of servo that you use, SERVO_ANGLE or SERVO_COMTINUOUS
    servod_path : str
        Path to the "servod" executable

    """

    def __init__(self, pin=0, type=SERVO_ANGLE, servod_path=SERVOD_PATH):
        self.pin = pin
        self.servod_path = servod_path
        if type == SERVO_ANGLE:
            self.range = (0.08,0.3)
        else:
            self.range = (0.131,0.161)

        if not self._servoblaster_started():
            self.start()

    def set(self, pulse_width):
        """
        Parameters
        ----------
        pulse_width : int
            pulse width to send to the servo measured in 10s of us
        """
        os.system('echo "{}={}" > /dev/pi-blaster'.format(self.pin, pulse_width))

    # 0 = Backwards, 0.5 = Stopped, 1 = Forwards
    def set_normalized(self, val):
        min, max = self.range
        scale = max - min
        speed = min + scale * val
        self.set(str(speed))

    def start(self):
        os.system('sudo {}'.format(self.servod_path))

    def stop(self):
        servod_name = os.path.split(self.servod_path)[1]
        os.system('sudo killall {}'.format(servod_name))

    def _servoblaster_started(self):
        servod_name = os.path.split(self.servod_path)[1]
        return servod_name in os.popen('ps -u root').read()


#servo_left = Servo(pins.SERVO_LEFT_MOTOR)
#servo_right = Servo(pins.SERVO_RIGHT_MOTOR)

#servo_left.set_normalized(1)
#servo_right.set_normalized(1)

#time.sleep(1)

#servo_left.set_normalized(0.5)
#servo_right.set_normalized(0.5)

#servo_left.stop()
