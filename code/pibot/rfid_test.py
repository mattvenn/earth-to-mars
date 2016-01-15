from arduino import Commands, Arduino
from time import sleep
from motors import Motors
from mission import Mission

mission = Mission()
board = Arduino()
board.connect()
move = Motors()

mission.waitForButton()
print("ok")

move.forward(60)
sleep(4)
move.stop()
sleep(2)
print("sampling")
location = mission.getLocation()
sample = mission.takeSample(location)

print(sample)

mission.endMission()
