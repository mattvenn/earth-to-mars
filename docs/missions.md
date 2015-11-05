# Training Missions

Training missions are carried out on the desk and get the children familiar with the robot’s capabilities and Python.

To get started, double click on the Idle2 icon.

## 0 - Hello Python!

The numbers on the left are line numbers and don't need to be typed in.
The codes on the right are Python commands and they have to be copied exactly as written. Make sure you copy all the symbols, and that everything is in the correct case.

In Idle, click `file -> new`. Type the following into the new window:

~~~ { .python .numberLines }
print("Earth to Mars!")
~~~

Then `click file -> save`. Save the file as `training0.py`. Then click `run -> run module`.

## 1 - Basic robot movement

* Move forwards 10cm and back 10cm.
* Programming concepts required: sequence.

This program introduces you to the basic movements of the robot. Make a new file, then copy this program into the file:

~~~ { .python .numberLines }
from arduino import Commands, Arduino
from time import sleep
from motors import Motors

board = Arduino()
board.connect()
move = Motors()

print("forward")
move.forward(50)
sleep(1)
move.stop()

sleep(1)

print("backward")
move.backward(50)
sleep(1)
move.stop()

~~~

Now save the file as `training1.py` and then run the program to see the robot move.

## 2 - M for Mars

* Program the robot to trace out an M shape.
* Programming concepts required: sequence.

Modify your program to draw an M shape with the robot. Save it as `training2.py`. You'll need to know how to turn the motor. This is done by driving one motor forwards, and the other backwards:

~~~ { .python .numberLines }
print("turn")
move.leftMotor(50, 1) #  the first number is speed, the second is direction
move.rightMotor(50, 0)
sleep(1)
move.stop()
~~~

## 3 - Timelapse

* Use the robot’s camera to take a photo every few seconds.
* Programming concepts required: loops.

This program uses a loop to print out the numbers 1 to 10:

~~~ { .python .numberLines }
num = 0
while num < 10:
    print(num)
    num = num + 1
~~~

And this program takes a photo, saving the output to a numbered file:

~~~ { .python .numberLines }
import picamera

num = 0
with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    time.sleep(2)
    camera.capture("%03d.jpg" % num) 
~~~

## 4 - Obstacle avoidance

NB. Ultrasound isn't working.

* Use the robot’s ultrasonic detectors to stop the robot hitting a wall.
* Programming concepts required: conditionals.

This program shows how to find out how far something is away from the ultrasonic detector:

~~~ { .python .numberLines }
from arduino import Commands
from arduino import Arduino
from ultrasound import Ultrasound
from time import sleep

board = Arduino()
board.connect()

print "Getting ultrasound distance"
ultra = Ultrasound()
print(ultra.getDistance())
~~~

See if you can adapt it so that every second it reads the sensor and prints the distance.

Here's a way of making a loop that never ends:

~~~ { .python .numberLines }
while True:
    # do something
~~~

To stop the loop, choose the window titled 'shell' and press `control` and `c` at the same time.

## 5 - Starting a mission with the button

All the training missions have been completed with the robot on the desk in front of you. When your robot is in the Mars yard, you won't have access to it.

After landing in the Mars yard, the button on the robot will be pressed, so it knows to start the mission. 

Here's how you wait for a button:

~~~ { .python .numberLines }
import mission

mission.wait_for_button() #  turns on the LED and waits for the button
print("hello!")
~~~

Write a short program that waits for the button and then drives the robot forward. 

## 5 - Saving and reading transmissions

* Take a temperature sample and send the data. Then receive the data and check it’s correct.
* Programming concepts required: data

After your robot has completed a mission, it will probably need to save some data that you can look at later. The data might be a photo, or it might be a temperature or a gas measurement.

Here's how you can save a measurement while the robot is in the Mars Yard, so you can read it later:

~~~ { .python .numberLines }
import mission

data = 10.5
mission.delete_data(data)  # delete old data
mission.save_data(data)  # save some new data into a file called mission.txt
~~~

To read the data afterwards you can open the `mission.txt` file by using the file manager and double clicking the file.

# Mars Missions

## 1 - Drive to a location and return.

* Difficulty: 1/5
* Curriculum links: use a sequence of instructions to program a computer. Use two or more programming languages, at least one of which is textual, to solve a variety of computational problems.
* STEM links: engineering

The training missions should give you enough to get going on your first mission. 

Tips:

* Test your program on your desk.
* Save your program as mission1.py
* Use `mission.wait_for_button()` so the program can be started in the Mars Yard
* Start your program running
* Unplug the keyboard, mouse and monitor before taking your robot to the launch location.

Good luck!

## 2 - Drive to a location, take a sample.

* Sample consists of: H2, temperature, humidity and location.
* Difficulty: 2/5
* Curriculum links: can analyse problems in computational terms
* STEM links: engineering, science

Here's how you can take samples:

~~~ { .python .numberLines }
from arduino import Commands
from arduino import Arduino
from etm import ETMSensors

sensors = ETMSensors()

h2 = sensors.getH2()
temp = sensors.getTemp()
humidity = sensors.getHumidity()
~~~

To find your location, you need to point the camera straight up and take a photo. By looking at the number in the middle of the photo you can determine your location.

You already know how to take a photo, here's how to aim the camera:

~~~ { .python .numberLines }
TODO
~~~

## 3 - Upload sample data to group database.

* Using sample data from activity 2, upload to a projected map of overlaid data. The more teams that complete this mission, the clearer picture will be of where signs of life could be found.
* Difficulty: 2/5
* Curriculum links: undertake creative projects that involve selecting, using, and combining multiple applications, preferably across a range of devices, to achieve challenging goals, including collecting and analysing data and meeting the needs of known users.
* STEM links: science, maths

If your previous mission was a success, you will have a photo and some data in `mission.txt`.

Double click the photo and work out the number that's closest to the centre, this is your position number.
Look at the contents of `mission.txt`. To submit your samples to the group database, open the web browser and go to `http://mission.control/submit`.

Enter your location and sample values into the fields and then press `submit`.

You can see the results of all the data on the big mission control screen, or go to `http://mission.control`. Where do you think the best places are to search for life? Why?

## 4 - Enter an area of shadow and return.

* Explore dark area and return to sunlight for solar battery charging.
* Difficulty: 3/5
* Curriculum links: can evaluate and apply information technology, including new or unfamiliar technologies, analytically to solve problems
* STEM links: engineering

The Mars rover charges its batteries using solar panels. This makes going into dark places dangerous, because it could get stuck if the batteries get flat.

In this mission, you'll use the camera to find somewhere dark, then drive somewhere light to charge your batteries.

You already know how to take a photo, this code shows how to process the image to get a value between completely dark (0) and completely white (255).

~~~ { .python .numberLines }
import mission
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    time.sleep(2)
    camera.capture("image.jpg") 

value = mission.process_image("image.jpg")

if value < 50:
    print("dark")
elif value > 150:
    print("light")
else:
    print("medium")
~~~

## 5 - Find an unknown obstacle using distance sensors and take a photo

* Difficulty: 5/5
* Curriculum links: design, use and evaluate computational abstractions that model the state and behaviour of real-world problems and physical systems. Understand several key algorithms that reflect computational thinking
* STEM links: engineering, maths.

Ultrasound isn't working yet, if it works then participants drive to a place where they are close to the wall, take a photo looking forwards, and one up. Then upload the data to mission control. Mission control will build a panarama from the location and the picture.

## 6 - Averaging

* Single samples are often not accurate, so often multiple samples are taken and then averaged. Write a program that takes averages of your samples.
* Difficulty: 4/5

Tips:

* Use a loop that counts up to a certain number (let's say 10),
* Take a sample in the loop, and add it to a total, 
* Wait for some time,
* Repeat the loop
* After the loop, divide the total by your number (10 in this case).

The more samples you take, the more accurate the measurement.

## 7 - Multi sample

* Program a route for the robot to take, and take many samples along the route. Store all the samples along with their locations. At mission control, upload all the samples.
* Difficulty: 5/5

If you're sampling multiple sensors lots of times, you probably want to split the data up into separate files. That way we can write a program to upload them all to mission control automatically.

Before if you had some data in a variable called `data`, you could use `mission.save_data(data)` to save the data in a file called `mission.txt`.

If you pass another parameter called `file`, you can get `mission.save` to save the data into separate files:

~~~ { .python .numberLines }
h2 = sensors.getH2()
temp = sensors.getTemp()
humidity = sensors.getHumidity()
mission.save(h2, file="h2.txt")
mission.save(temp, file="temp.txt")
mission.save(humidity, file="humidity.txt")
~~~

This will result in 3 separate files, all with their own data.

Tips:

* For each sample, take a numbered photograph of the location map.
* When the robot returns, you'll need to upload each sample with its location.

For our automatic uploading program, we need a new file that contains all the locations of all the samples.

Create a new file called `locations.txt`. Go through each photo and write the central number down in the file.

Check that all your files have the same number of lines. 

This program shows how you could upload all your temperatures:

~~~ { .python .numberLines }
# read all the temperatures into a list called temps
with open("temperatures.txt") as fh:
    temps = fh.readlines()

# read all the locations into a list called locations
with open("locations.txt") as fh:
    locations = fh.readlines()

for temp, loc in zip(temps, locations)
    mission.upload(type="temp", data=temp, location=loc)
~~~

Adapt this program to upload all your samples.
