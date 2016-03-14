import paho.mqtt.client as mqtt
import glob, os
import time
import socket

"""
when receives mqtt message /missioncontrol/shutdown
this program will:
    delete a bunch of files from ~/
    shutdown the computer
"""

def cleanup():
    print("about to remove all student files from /home/pi/")
    files = glob.glob(os.path.expanduser('/home/pi/*'))

    for file in files:
        print("removing %s" % file)
        try:
            os.remove(file)
        except OSError:
            pass

def halt():
    print("halt")
    os.system('sudo halt')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/missioncontrol/#")

def on_message(client, userdata, msg):
    if msg.topic == '/missioncontrol/cleanup':
        cleanup()
    if msg.topic == '/missioncontrol/halt':
        halt()
    else:
        print(msg.topic+" "+str(msg.payload))
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

while True:
    try:
        client.connect("mission.control", 1883, 60)
        client.loop_forever()
        break
    except socket.error:
        print("no network")
        time.sleep(5)
    except KeyboardInterrupt as e:
        print("ending")
