from pibot.arduino import Arduino
from pibot.motors import Motors
from pibot.ultrasound import Ultrasound
from pibot.mission import Mission
from time import sleep
import picamera

board = Arduino()
board.connect()
ultra = Ultrasound()
move = Motors()

mission = Mission()

# wait for the button to be pressed
mission.startMission() 

while True:
    # drive for 1 second at 50% power
    move.forward(50)
    sleep(1) 
    move.stop()

    # measure the distance
    distance = ultra.getDistance()
    print(distance)

    if distance <= 20:
        # take the photo
        print("taking photo")
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.hflip = True
            camera.vflip = True
            camera.capture("photo.jpg") 

        # find the location
        location = mission.getLocation()
        sample = mission.takeSample(location)

        # save the location
        mission.deleteData()
        mission.saveData(sample)

        # stop the loop
        break;
    

# end the mission
mission.endMission()
