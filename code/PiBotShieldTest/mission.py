import RPi.GPIO as GPIO
import time
import os
from PIL import Image, ImageStat
GPIO.setmode(GPIO.BOARD)
RED_LED_GPIO = 26
GREEN_LED_GPIO = 29
BUTTON = 36

data_file = "mission.txt"

GPIO.setup(GREEN_LED_GPIO,GPIO.OUT)
GPIO.setup(RED_LED_GPIO,GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def waitForButton():

    GPIO.output(GREEN_LED_GPIO,False)
    GPIO.output(RED_LED_GPIO,True)
    print("waiting for button...")
    while GPIO.input(button) == False:
        time.sleep(0.1)
    GPIO.output(RED_LED_GPIO,False)

def endMission():
    GPIO.output(GREEN_LED_GPIO,True)

def deleteData():
	try:
		os.unlink(data_file)
	except OSError:
		pass


def saveData(data):
	with open(data_file,'a') as fh:
		fh.write(str(data) + "\n")


def process(file_name):
    im = Image.open(file_name).convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]


if __name__ == '__main__':
    wait_for_button()	
    delete_data()
    save_data(10.0)
    save_data("Mars")

    for filename in ['black','grey','white']:
        print(filename, process(filename + ".jpg"))
