from umqtt.simple import MQTTClient
import dht
import machine
import time
import ujson

from wifi import connect_wifi

DHT_PIN = 4

BROKER = "YOUR_LAPTOP_IP"
PORT = 1883
TOPIC = b"iot/lab/sensor"
CLIENT_ID = "esp32_dht22_client"

sensor = dht.DHT22(machine.Pin(DHT_PIN))

connect_wifi()

client = MQTTClient(CLIENT_ID, BROKER, port=PORT)
client.connect()

print("Connected to MQTT broker")

while True:
    try:
        sensor.measure()

        payload = {
            "temperature": sensor.temperature(),
            "humidity": sensor.humidity()
        }

        message = ujson.dumps(payload)

        client.publish(TOPIC, message)

        print("Published:", message)

    except Exception as e:
        print("Error:", e)

    time.sleep(5)