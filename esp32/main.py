import dht
import machine
import time

DHT_PIN = 4

sensor = dht.DHT22(machine.Pin(DHT_PIN))

while True:
    try:
        sensor.measure()

        temperature = sensor.temperature()
        humidity = sensor.humidity()

        print("Temperature:", temperature)
        print("Humidity:", humidity)
        print("--------------------")

    except Exception as e:
        print("Sensor error:", e)

    time.sleep(2)