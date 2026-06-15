from umqtt.simple import MQTTClient
from machine import unique_id
from ubinascii import hexlify

# =========================================================
# MQTT Configuration
# =========================================================

# Public MQTT broker used for the lab.
BROKER = "broker.hivemq.com"
PORT = 1883

# Unique topic for our group.
TOPIC = b"iot/lab/group2"

# Unique client ID prevents conflict with other ESP32 devices.
CLIENT_ID = b"esp32-dht22-" + hexlify(unique_id())


def connect_mqtt():
    """
    Connect the ESP32 to the MQTT broker.
    Returns the connected MQTT client.
    """

    print("Connecting to MQTT broker:", BROKER)
    print("Client ID:", CLIENT_ID.decode())

    client = MQTTClient(
        client_id=CLIENT_ID,
        server=BROKER,
        port=PORT,
        keepalive=60
    )

    client.connect()

    print("MQTT connected successfully")
    print("Publishing to topic:", TOPIC.decode())

    return client


def publish_sensor_data(client, payload):
    """
    Publish a JSON payload to the MQTT topic.
    """

    client.publish(TOPIC, payload)
    print("Published:", payload)