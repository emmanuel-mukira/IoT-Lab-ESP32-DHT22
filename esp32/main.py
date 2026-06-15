import dht
import machine
import time
import ujson

from wifi import connect_wifi
from mqtt_publish import connect_mqtt, publish_sensor_data


# =========================================================
# SENSOR CONFIGURATION
# =========================================================
DHT_PIN = 4

# Publish every 3 seconds.
# This is fast enough to collect 10+ messages quickly during the lab.
PUBLISH_INTERVAL = 3

# Device name used in JSON and database.
DEVICE_NAME = "ESP32-DHT22"

sensor = dht.DHT22(machine.Pin(DHT_PIN))

message_counter = 0
start_time = time.ticks_ms()


def read_sensor():
    """
    Reads temperature and humidity from the DHT22 sensor.
    Returns temperature and humidity.
    """

    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    return temperature, humidity


def create_payload(temperature, humidity):
    """
    Creates the JSON message sent through MQTT.
    This matches the improved database schema on the laptop side.
    """

    global message_counter

    message_counter += 1

    uptime_seconds = time.ticks_diff(time.ticks_ms(), start_time) // 1000

    payload = {
        "device": DEVICE_NAME,
        "message_no": message_counter,
        "temperature": temperature,
        "humidity": humidity,
        "uptime_seconds": uptime_seconds
    }

    return ujson.dumps(payload)


def main():
    print("=" * 50)
    print("ESP32 DHT22 MQTT Publisher")
    print("=" * 50)

    # Step 1: Connect to WiFi.
    connect_wifi()

    # Step 2: Connect to MQTT broker.
    client = connect_mqtt()

    print("DHT22 sensor initialized on GPIO", DHT_PIN)
    print("Starting sensor readings...")
    print("Press Ctrl+C in Thonny to stop.")
    print("=" * 50)

    while True:
        try:
            temperature, humidity = read_sensor()

            payload = create_payload(temperature, humidity)

            print("Message No:", message_counter)
            print("Temperature:", temperature)
            print("Humidity:", humidity)

            publish_sensor_data(client, payload)

            print("-" * 50)

        except OSError as e:
            print("Sensor read error:", e)
            print("Check DHT22 wiring, DATA pin, and 10k resistor.")

        except Exception as e:
            print("General error:", e)
            print("Trying to continue...")

        time.sleep(PUBLISH_INTERVAL)


main()