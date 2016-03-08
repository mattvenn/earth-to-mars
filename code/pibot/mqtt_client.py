import paho.mqtt.client as mqtt

def shutdown():
    print("removing all student files")

    print("halt")

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

client.connect("mission.control", 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt as e:
    print("ending")

