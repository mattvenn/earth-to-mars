# these 3 lines import some libraries that the software uses
from pibot.arduino import Arduino
from pibot.motors import Motors
from pibot.mission import Mission
from time import sleep

# these 3 lines get the robot setup and ready to go
board = Arduino()
board.connect()
move = Motors()

mission = Mission()

# wait for the button to be pressed
mission.startMission() 

# drive forwards for 3 seconds at 50% power
move.forward(50)
sleep(3) 
move.stop()

# take a sample
location = mission.getLocation()
sample = mission.takeSample(location)

# delete the old data
mission.deleteData()

# save the sample
mission.saveData(sample)

# end the mission
mission.endMission()
