import time
import os
import json
import requests

pi = os.environ.get("NO_PI_TEST", True)
if pi is True:
    from arduino import Arduino, Commands
    from motors import Motors
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    RED_LED_GPIO = 26
    GREEN_LED_GPIO = 29
    BUTTON = 36

data_file = "mission.txt"
rfid_hash = os.path.join(os.path.dirname(__file__), "sample_data.json")
mc_url = "http://mission.control"

class Mission():
    
    # tested
    def __init__(self):

        if pi is True:
            self.board = Arduino()
            self.board.connect()
            self.move = Motors()
            GPIO.setup(GREEN_LED_GPIO,GPIO.OUT)
            GPIO.setup(RED_LED_GPIO,GPIO.OUT)
            GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # load the sample hash
        with open(rfid_hash) as fh:
            self.rfid_hash = json.load(fh)


    # won't test
    def startMission(self):
        if pi is True:
            GPIO.output(GREEN_LED_GPIO,False)
            GPIO.output(RED_LED_GPIO,True)
            print("waiting for button...")
            while GPIO.input(BUTTON) == False:
                time.sleep(0.1)
            GPIO.output(RED_LED_GPIO,False)

    # won't test
    def endMission(self):
        if pi is True:
            GPIO.output(GREEN_LED_GPIO,True)

    # tested
    def deleteData(self):
        try:
            os.unlink(data_file)
        except OSError:
            pass

    # tested
    # stores a dict as json on the disk
    # appends to the data file
    def saveData(self, sample):
        with open(data_file,'a') as fh:
            fh.write(json.dumps(sample) + "\n")

    # tested
    # returns a list of dicts
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
    # fetches an RFID
    def getLocation(self):
        if pi is True:
            rfid = ""
            # keep moving until robot gets a location
            while True:
                rfid = self.board.sendCommand(Commands.READ_RFID,0,0)
                # when I catalogued the RFIDs I missed the last char!
                rfid = rfid[0:11]
                if len(rfid) == 11:
                    break
                self.move.forward(70)  
                time.sleep(0.1)
                self.move.stop()
                time.sleep(1)
            return rfid
    
    # tested
    # indexes into the sample database with the RFID and returns sample as dict
    def takeSample(self, location):
        try:
            return self.rfid_hash[location]
        except KeyError:
            raise Exception("unknown location [%s]" % location)

    # tested
    # uploads a sample dict with a team name (string)
    def uploadSample(self, sample, team):
        # fetch team ID from nane
        r = requests.get(mc_url + '/api/team/' + team)
        if r.status_code == 400:
            raise Exception(r.text)

        team_id = json.loads(r.text)['id']
        sample['team'] = str(team_id)

        # posts it
        r = requests.post(mc_url + '/api/sample', json=sample)
        if r.status_code == 400:
            return r.text
            #exeception stops the program
            #raise Exception(r.text)

        new_sample = json.loads(r.text)
        print("uploaded sample %d" % new_sample['id'])
        return new_sample
    
    def getAllSamples(self):
        r = requests.get(mc_url + '/api/samples')
        samples = json.loads(r.text)['samples']
        return samples


if __name__ == '__main__':
    mission = Mission()
    mission.startMission()	

    while True:
        try:
            rfid = mission.getLocation()
            sample = mission.takeSample(rfid)
            print sample
        except Exception as e:
            print e
        time.sleep(1.0)
