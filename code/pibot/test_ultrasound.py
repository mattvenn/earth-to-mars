from pibot.arduino import Arduino
from pibot.ultrasound import Ultrasound
from time import sleep
import picamera

board = Arduino()
board.connect()
ultra = Ultrasound()

print("testing ultrasound")

while True:
    distance = int(ultra.getDistance())
    print(distance)

    if distance <= 20:
        print("taking photo")
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.hflip = True
            camera.vflip = True
            camera.capture("photo.jpg") 
            break;
    
    time.sleep(0.5)
