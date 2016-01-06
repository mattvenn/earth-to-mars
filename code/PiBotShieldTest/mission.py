import RPi.GPIO as GPIO
import time
import os
from PIL import Image, ImageStat
GPIO.setmode(GPIO.BOARD)

data_file = "mission.txt"

def wait_for_button():
	button = 36
	RED_LED_GPIO = 26

        GPIO.setup(RED_LED_GPIO,GPIO.OUT)
	GPIO.output(RED_LED_GPIO,True)
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	print("waiting for button...")
	while GPIO.input(button) == False:
		time.sleep(0.1)
	GPIO.output(RED_LED_GPIO,False)

def delete_data():
	try:
		os.unlink(data_file)
	except OSError:
		pass


def save_data(data):
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
