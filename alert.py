import paho.mqtt.client as mqtt
import limits
import asyncio

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    client.subscribe("#")

def on_message(client, userdata, msg):
    for alert in limits.limits:
        alert.test(msg.topic, msg.payload)
    


async def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    client.loop_start()

    await limits.watchdog(limits.limits)
    

asyncio.run(main())

