import json
import sqlite3
from pathlib import Path
from datetime import datetime

import paho.mqtt.client as mqtt


# =========================================================
# MQTT Configuration
# =========================================================

# Public MQTT broker.
# This must match the broker used by the ESP32.
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "iot/lab/group2"


# =========================================================
# SQLite Configuration
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sensor_data.db"


def create_database():
    """
    Create the SQLite database table if it does not already exist.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT,
            message_no INTEGER,
            temperature REAL,
            humidity REAL,
            uptime_seconds INTEGER,
            mqtt_topic TEXT,
            received_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_to_database(data, topic):
    """
    Save received MQTT sensor data into the SQLite database.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    device = data.get("device", "ESP32-DHT22")
    message_no = data.get("message_no")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    uptime_seconds = data.get("uptime_seconds")
    received_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO sensor_data (
            device,
            message_no,
            temperature,
            humidity,
            uptime_seconds,
            mqtt_topic,
            received_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        device,
        message_no,
        temperature,
        humidity,
        uptime_seconds,
        topic,
        received_at
    ))

    conn.commit()
    conn.close()

    print("Saved to database:")
    print("Device:", device)
    print("Message No:", message_no)
    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Uptime Seconds:", uptime_seconds)
    print("Topic:", topic)
    print("Received At:", received_at)
    print("-" * 60)


def show_latest_rows():
    """
    Show the latest 5 saved records for quick verification.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, device, message_no, temperature, humidity, uptime_seconds, received_at
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()
    conn.close()

    print("Latest database rows:")
    for row in rows:
        print(row)

    print("-" * 60)


def on_connect(client, userdata, flags, rc):
    """
    Runs when the laptop connects to the MQTT broker.
    """

    if rc == 0:
        print("Connected to MQTT broker:", BROKER)
        client.subscribe(TOPIC)
        print("Subscribed to topic:", TOPIC)
        print("Waiting for ESP32 messages...")
        print("-" * 60)
    else:
        print("Connection failed with code:", rc)


def on_message(client, userdata, msg):
    """
    Runs whenever a message is received from the MQTT topic.
    """

    try:
        payload = msg.payload.decode("utf-8")

        print("Message received")
        print("Topic:", msg.topic)
        print("Raw payload:", payload)

        data = json.loads(payload)

        save_to_database(data, msg.topic)
        show_latest_rows()

    except json.JSONDecodeError:
        print("Invalid JSON received. Message was not saved.")
        print("Payload was:", msg.payload.decode("utf-8", errors="ignore"))

    except Exception as e:
        print("Error while processing message:", e)


def main():
    """
    Start the MQTT subscriber and save incoming messages to SQLite.
    """

    create_database()

    print("Database ready:", DB_PATH)
    print("Connecting to MQTT broker:", BROKER)

    client = mqtt.Client(client_id="pc-sqlite-subscriber")

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)

    print("Subscriber running. Press Ctrl + C to stop.")
    print("-" * 60)

    client.loop_forever()


if __name__ == "__main__":
    main()