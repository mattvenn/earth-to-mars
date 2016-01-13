# The Mars Explorer Robot

To use your robot, you'll need to make the following connections shown in the
photo below:

* microusb for charging the battery
* hdmi for video
* usb for keyboard and mouse

# TODO photo here

The first time the robot is plugged in you will see the computer loading on the
screen. After a while you will see a login screen. The username is `pi` and the
password is `raspberry`.

# Training Missions

The following training missions will get you prepared for the real missions.

To get started, double click on the Idle2 icon.

## 0 - Hello Python!

The numbers on the left are line numbers and don't need to be typed in.
The codes on the right are Python commands and they have to be copied exactly as written. Make sure you copy all the symbols, and that everything is in the correct case.

In Idle, click `file -> new window`. Type the following into the new window:

~~~ { .python .numberLines }
print("Earth to Mars!")
~~~

Then `click file -> save`. Save the file as `training0.py`. Then click `run -> run module`.

## 1 - Basic robot movement

* Move forwards 10cm and back 10cm.
* Programming concepts required: sequence.

This program introduces you to the basic movements of the robot. Make a new
file, then copy this program into the file. You don't need to copy the lines
that start with a `#`, they are to tell you what the program is doing:

~~~ { .python .numberLines }
# these 3 lines import some libraries that the software uses
from arduino import Commands, Arduino
from time import sleep
from motors import Motors

# these 3 lines get the robot setup and ready to go
board = Arduino()
board.connect()
move = Motors()

# the rest of the program shows how to move the robot around
print("forward")
move.forward(50)  # 50 is the speed. It goes from 0 to 100
sleep(1)  # 1 is the number of seconds to wait
move.stop()

sleep(1)

print("backward")
move.backward(50)
sleep(1)
move.stop()

~~~

Now save the file as `training1.py` and then run the program to see the robot move.

How slow can you make the robot go?

## 2 - Turning

* Program the robot to turn around
* Programming concepts required: sequence.

Modify your program to make the robot turn around by 180 degrees. Save it as
`training2.py`. To turn the robot, you can drive one motor forwards, and the other backwards:

~~~ { .python .numberLines }
print("turn")
move.leftMotor(50, 1) #  the first number is speed, the second is direction
move.rightMotor(50, 0)
sleep(1)
move.stop()
~~~

## 3 - Photo

* Use the robot’s camera to take a photo

This program takes a photo, saving the output to a file:

~~~ { .python .numberLines }
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.capture("photo.jpg") 
~~~

Write a program that can take a photo of your team and use the file browser to
look at the photo.

\ ![file browser](filemanager.png)

## 4 - Obstacle avoidance

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

Add a `conditional` to your program so that when the robot is within 20cm of an
obstacle it prints a message on your screen. Here's how you can make a simple
`if` conditional work:

~~~ { .python .numberLines }
# make a variable called distance and store the distance in it
distance = ultra.getDistance()
if distance < 50:
    print("obstacle detected!")
~~~

## 5 - Starting a mission with the button

All the training missions have been completed with the robot on the desk in front of you. When your robot is in the Mars yard, you won't have access to it.

After landing in the Mars yard, you'll press the  button on the robot, so it knows to start the mission. 

Here's how you wait for a button:

~~~ { .python .numberLines }
from mission import Mission

mission.waitForButton() #  turns on the red and waits for the button
print("hello!")
mission.end() # turns on the green led.
~~~

Write a short program that waits for the button and then drives the robot
forward. Copy the code that moves the robot from a previous training mission.

## 6 - Saving and reading transmissions

* Take a sample and send the data. Then receive the data and check it’s correct.
* Programming concepts required: data

After your robot has completed a mission, it will probably need to save some
data that you can look at later. 

Here's how you can save a measurement while the robot is in the Mars Yard, so you can read it later:

~~~ { .python .numberLines }
from mission import Mission

mission.deleteData()      # delete old data

location = mission.getLocation() 
sample = mission.takeSample(location)

mission.saveData(sample)  # save the sample
~~~

To read the data afterwards you can open the `mission.txt` file by using the
file manager and double clicking the file. The data is stored separated by
commas. So `mission.txt` might look like:

    {"temperature": 200.0, "oxygen": 0.06, "humidity": 100.0, "y": 16, "x": 10, "methane": 0.03}

# Mars Missions

## 1 - Drive to a location, take a sample.

* A sample consists of: Methane, Oxygen, Temperature and Humidity.
* Difficulty: 2/5

Here's how you can take samples:

~~~ { .python .numberLines }
from arduino import Commands
from arduino import Arduino
from mission import Mission

mission = Mission()
location = mission.getLocation()
sample = mission.takeSample(location)
print(sample)
~~~

Tips:

* Test your program on your desk (you won't get a sample because the robot isn't
 on Mars yet!
* Save your program as mission1.py
* Make sure you save your sample and the location using the technique shown in training mission
 6
* Use `mission.waitForButton()` so the program can be started in the Mars Yard
* Start your program running
* Unplug the keyboard, mouse and monitor before taking your robot to the launch
* Press the button once the robot is in the Mars Yard

Given that Mars doesn't have a GPS system, how do you think the real Mars robot
works out its position? 

Use the Midori web browser to answer the question at `http://mission.control/questions/1` 

\ ![browser](web_browser.jpg)

## 2 - Upload sample data to group database.

* Using sample data from activity 1, upload your data to mission control. The more teams that complete this mission, the clearer picture will be of where signs of life could be found.
* Difficulty: 2/5

If your previous mission was a success, you will have some data in `mission.txt`.

Look at the contents of `mission.txt`. To upload your samples to the group
database, open the web browser and go to `http://mission.control/upload/sample`.

Enter your location and sample values into the fields and then press `upload`.

You can see the results of all the data on the big mission control screen, or go
to `http://mission.control`. Where do you think the best places are to search
for life? Why? 

Answer the question at `http://mission.control/questions/2`

## 3 - Find an unknown obstacle using distance sensors and take a photo

* Difficulty: 5/5

Use your ultrasound sensor to detect where the edges of the Mars Yard are. Drive
to 20cm away and take a photo pointing forwards. Use your skills to store the
robot's location when the photo was taken.

When your robot returns, upload the photo to `http://mission.control/upload/photo`.

Mission control will build a panorama of the images as more are uploaded.

How many photos do you think the real robot takes in a day? How many of those do
you think get sent back to Earth for analysis by scientists? 

Answer the question at `http://mission.control/questions/4`

## 4 - Averaging

* Single samples are often not accurate, so often multiple samples are taken and then averaged. Write a program that takes averages of your samples.
* Difficulty: 4/5

Tips:

* Use a loop that counts up to a certain number (let's say 10),
* Take a sample in the loop, and add it to a total, 
* Wait for some time,
* Repeat the loop
* After the loop, divide the total by your number (10 in this case).

Here's how you can write a loop that does something 10 times:

~~~ { .python .numberLines }
num = 0             # make a variable called num
while num < 10:     # while num is less than 10
    print(num)      # print it
    num = num + 1   # add one to num
~~~

The part of the loop that is repeated has been indented. This should
automatically happen after you type the `:` character.

The more samples you take, the more accurate the measurement.

How many samples do you think you should take for temperature, humidity and
hydrogen? Why?

Answer the question at `http://mission.control/questions/4`

## 5 - Multi sample

* Program a route for the robot to take, and take many samples along the route. Store all the samples along with their locations. At mission control, upload all the samples.
* Difficulty: 5/5

If you're sampling multiple sensors lots of times, you probably won't want to
upload all the data manually. We will write a program to upload all the data
automatically.

Tips:

* For each sample, use 
* When the robot returns, you'll need to upload each sample with its location.

This program shows how you could print all your samples:

~~~ { .python .numberLines }
# read all the samples into a list called data
data = mission.loadData()

# go through each sample the robot took and print it out
for sample in data:
    print(sample)
~~~


We can now use a new function called `uploadSample()` that will upload each sample to the group database.

Here's how you can use it (imagine your team name is 'Earth'):

    mission.uploadSample(sample, 'Earth')

Adapt this program to upload all your samples automatically.

Do you think the robot sends back all its samples or just some of them. Why?

Answer the question at `http://mission.control/questions/5`

## 6 - Process data

* Write a program that downloads all the data for a measurement and make an
 average.
* Difficulty: 5/5

There should be a lot of samples now uploaded to Mission Control. It would be
good to know the average amounts of each type of sample.

You can use the following to download all the data for a given sample:

~~~ { .python .numberLines }
# fetch all the samples
samples = mission.getAllSamples()

# samples is a type of variable called a list, we can loop through it like this:
for sample in samples:
    # print it out
    print(sample)

    # print just the methane amount
    print(sample['methane'])
~~~

Adapt the program to print out the total number of samples, and the average of
each type of sample.

If the robot sends back 10,000 samples, do you think scientists look at them all
individually or use a computer to analyse them? Why?

Answer the question at `http://mission.control/questions/6`
