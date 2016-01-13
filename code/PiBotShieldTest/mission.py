import time
import os
import json
import requests
from arduino import Commands
from arduino import Arduino


data_file = "mission.txt"
rfid_hash = "sample_data.json"

class Mission():
    
    # tested
    def __init__(self, pi=True):

        self.board = Arduino()
        self.board.connect()

        self.pi = pi
        if self.pi:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BOARD)
            RED_LED_GPIO = 26
            GREEN_LED_GPIO = 29
            BUTTON = 36

        # load the sample hash
        with open(rfid_hash) as fh:
            self.rfid_hash = json.load(fh)

        if self.pi:
            self.board = Arduino()
            self.board.connect()
            GPIO.setup(GREEN_LED_GPIO,GPIO.OUT)
            GPIO.setup(RED_LED_GPIO,GPIO.OUT)
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # won't test
    def waitForButton(self):
        if self.pi:
            GPIO.output(GREEN_LED_GPIO,False)
            GPIO.output(RED_LED_GPIO,True)
        print("waiting for button...")
        if self.pi:
            while GPIO.input(button) == False:
                time.sleep(0.1)
            GPIO.output(RED_LED_GPIO,False)

    # won't test
    def endMission(self):
        if self.pi:
            GPIO.output(GREEN_LED_GPIO,True)

    # tested
    def deleteData(self):
        try:
            os.unlink(data_file)
        except OSError:
            pass

    # tested
    def saveData(self, sample):
        with open(data_file,'a') as fh:
            fh.write(json.dumps(sample) + "\n")

    # tested
    def loadData(self):
        data = []
        try:
            with open(data_file,) as fh:
                for sample in fh.readlines():
                    data.append(json.loads(sample))
        except IOError:
            pass
        return data

    # won't test
    def getLocation(self):
        if self.pi:
            return self.board.sendCommand(Commands.READ_RFID,0,0)
        return None
    
    # tested
    def takeSample(self, location):
        try:
            return self.rfid_hash[location]
        except KeyError:
            raise Exception("unknown location")

    # TODO
    def uploadSample(self, sample, team=None):
        sample['team'] = '1'
        sample['methane'] = sample['methane']
        sample['humidity'] = sample['humidity']
        sample['oxygen' ] = sample['oxygen']
        sample['temperature'] = sample['temperature'] 
        print(sample)
        r = requests.post('http://mission.control:5000/api/sample', json=sample)
        print r.text


if __name__ == '__main__':
    mission = Mission()
    mission.waitForButton()	

    while True:
        rfid = mission.getLocation()
        rfid = rfid.strip()
        if len(rfid) == 12:
            print("rfid=%s" % rfid)
        sleep(0.1)
