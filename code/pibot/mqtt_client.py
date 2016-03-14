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

def shutdown():
    files = []
    # individual files
    for file in ["mission.txt"]:
        print file
        files.append(os.path.expanduser('~/' + file))
    # globs
    for pat in ["*.py*", "*.jpg", "*.png"]:
        files += glob.glob(os.path.expanduser('~/' + pat))

    # remove them after a warning
    print("about to remove all student files from ~/. ^C to abort!")
    time.sleep(3)
    for file in files:
        print("removing %s" % file)
        try:
            os.remove(file)
        except OSError:
            pass

    print("halt")
    os.system('sudo halt')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/missioncontrol/#")

def on_message(client, userdata, msg):
    if msg.topic == '/missioncontrol/shutdown':
        shutdown()
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
