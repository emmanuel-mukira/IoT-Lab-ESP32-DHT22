import json
import sqlite3
from pathlib import Path

import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883
TOPIC = "iot/lab/sensor"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sensor.db"


def save_to_database(temperature, humidity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sensor_data (temperature, humidity)
        VALUES (?, ?)
        """,
        (temperature, humidity),
    )

    conn.commit()
    conn.close()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Connection failed with code: {rc}")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print("Received:", payload)

        data = json.loads(payload)

        temperature = data["temperature"]
        humidity = data["humidity"]

        save_to_database(temperature, humidity)

        print("Saved to database:", temperature, humidity)

    except json.JSONDecodeError:
        print("Invalid JSON received. Message was not saved.")
    except KeyError as e:
        print(f"Missing field in JSON: {e}")
    except Exception as e:
        print("Error:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()