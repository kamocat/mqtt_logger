import paho.mqtt.client as mqtt
import sqlite

log = sqlite.db('waterwall.db')

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    client.subscribe("#")

def on_message(client, userdata, msg):
    log.insert(msg.topic, msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("homebase", 1883, 60)

client.loop_forever()
