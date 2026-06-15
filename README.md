# IoT Lab: ESP32 DHT22 Temperature and Humidity Monitoring using MicroPython, MQTT, and SQLite

This project is an Embedded Systems and IoT practical implementation using an ESP32 microcontroller, a DHT22 temperature and humidity sensor, MicroPython, MQTT, and SQLite. The system reads live environmental data from the DHT22 sensor, publishes the readings over WiFi using MQTT, receives the messages on a PC through a Python subscriber, and stores the received data in a local SQLite database.

The project demonstrates a complete IoT data flow from physical sensor measurement to wireless communication and database persistence.

## Project Overview

The ESP32 is used as the IoT node. It is connected to a DHT22 sensor, which measures temperature and humidity. The ESP32 runs MicroPython code that reads the sensor values, connects to WiFi, formats the readings as JSON, and publishes them to an MQTT topic.

A Python subscriber script running on the PC listens to the same MQTT topic. When messages are received, the subscriber parses the JSON payload and saves the data into an SQLite database with timestamps.

The MQTT topic used in this project is:

```text
iot/lab/group2
```

The MQTT broker used for testing is:

```text
broker.hivemq.com
```

## System Architecture

The project follows this IoT data flow:

```text
DHT22 Sensor
    ↓
ESP32 Microcontroller
    ↓
MicroPython Sensor Reading
    ↓
WiFi Connection
    ↓
MQTT JSON Publishing
    ↓
MQTT Broker
    ↓
Python Subscriber on PC
    ↓
SQLite Database
    ↓
Stored Sensor Records
```

In simple terms, the sensor collects the data, the ESP32 sends the data, MQTT transports the data, the subscriber receives the data, and SQLite stores the data.

## Hardware Components

| Component               |  Quantity | Purpose                                                                |
| ----------------------- | --------: | ---------------------------------------------------------------------- |
| ESP32 Development Board |         1 | Main microcontroller used to read sensor data and publish it over WiFi |
| DHT22 / AM2302 Sensor   |         1 | Measures temperature and humidity                                      |
| Breadboard              |         1 | Used for circuit assembly                                              |
| Jumper Wires            | 3 or more | Used to connect the sensor to the ESP32                                |
| 10 kΩ Resistor          |         1 | Pull-up resistor for the DHT22 data line                               |
| USB Data Cable          |         1 | Used to connect the ESP32 to the PC                                    |

## Software and Tools Used

| Tool / Software      | Purpose                                                         |
| -------------------- | --------------------------------------------------------------- |
| MicroPython          | Programming environment running on the ESP32                    |
| Thonny IDE           | Used to communicate with the ESP32 and upload MicroPython files |
| esptool              | Used to detect, erase, and flash the ESP32                      |
| Python 3.x           | Used to run the PC-side subscriber scripts                      |
| paho-mqtt            | Python MQTT client library                                      |
| SQLite               | Local database used to store received sensor data               |
| Mosquitto CLI tools  | Used for MQTT testing and verification                          |
| HiveMQ Public Broker | Public MQTT broker used for message exchange                    |
| MQTTX                | Optional MQTT client used for testing messages                  |

## Repository Structure

```text
IoT-Lab-ESP32-DHT22/
│
├── documentation/
│   └── .gitkeep
│
├── esp32/
│   ├── main.py
│   ├── mqtt_publish.py
│   └── wifi.py
│
├── firmware/
│   └── ESP32_GENERIC.bin
│
├── screenshots/
│   ├── 1a.Group-Image.jpeg
│   ├── 1b.Group-Image 2.jpeg
│   ├── 2a.Driver-Installation.png
│   ├── 2b.ESP32-Port-detected.png
│   ├── 3a.Confirming-ESP32-communication-with-computer.png
│   ├── 3b.Erasing-ESP32-flash.png
│   ├── 3c.Writing-MicroPython-firmware-to-ESP32-flash.png
│   ├── 4a.Port-detected on thonny.png
│   ├── 4b.Thonny-communicating-with-ESP32.png
│   ├── 5a.Circuit-Connection1.png
│   ├── 5b.Circuit-Connection2.png
│   ├── 6a.Saving-code-files-to-ESP32.png
│   ├── 6b.Wifi-connected-successfully.png
│   ├── 6c.Wifi-error.png
│   ├── 7.Testing-DHT22-sensor.png
│   ├── 8a.MQTT-publishing.png
│   ├── 8b.MQTT-subscribing.png
│   └── 9.Data-from-DB.png
│
├── subscriber/
│   ├── create_db.py
│   ├── export_db_data.py
│   ├── sensor_data.db
│   ├── sensor_data_output.csv
│   ├── sensor_data_table.md
│   ├── subscriber.py
│   └── view_data.py
│
├── .gitignore
└── README.md
```

## Data Mapping: DHT22 to ESP32

The DHT22 sensor has three main connections used in this project: VCC, DATA, and GND. The sensor sends temperature and humidity readings through its DATA pin to the ESP32.

| DHT22 Pin      | ESP32 Pin            | Purpose                                          |
| -------------- | -------------------- | ------------------------------------------------ |
| VCC            | 3.3V                 | Powers the DHT22 sensor                          |
| DATA           | GPIO4                | Sends temperature and humidity data to the ESP32 |
| GND            | GND                  | Completes the electrical circuit                 |
| 10 kΩ Resistor | Between VCC and DATA | Pull-up resistor to stabilize the data signal    |

The DATA pin was mapped to GPIO4 in the MicroPython code. This means that the ESP32 reads the DHT22 sensor values from GPIO4.

The general data movement is:

```text
Temperature and humidity in the environment
    ↓
DHT22 sensor measures values
    ↓
DHT22 DATA pin sends signal
    ↓
ESP32 GPIO4 receives sensor signal
    ↓
MicroPython reads and processes the values
```

## Data Mapping: Sensor Reading to JSON Payload

After the ESP32 reads the temperature and humidity values, the readings are structured into a JSON message before being published through MQTT.

Example JSON payload:

```json
{
  "device": "ESP32-DHT22",
  "temperature": 27.9,
  "humidity": 59.5,
  "uptime": 65
}
```

| JSON Field  | Source                    | Description                                   |
| ----------- | ------------------------- | --------------------------------------------- |
| device      | ESP32 code                | Identifies the device publishing the data     |
| temperature | DHT22 temperature reading | Temperature value measured by the sensor      |
| humidity    | DHT22 humidity reading    | Humidity value measured by the sensor         |
| uptime      | ESP32 runtime counter     | Indicates how long the ESP32 has been running |

The MQTT topic used for publishing is:

```text
iot/lab/group2
```

## Data Mapping: MQTT Message to SQLite Database

The Python subscriber receives JSON messages from the MQTT broker and stores them in the SQLite database. Each incoming MQTT message is parsed and mapped to database columns.

| MQTT / JSON Data | SQLite Column | Description                                       |
| ---------------- | ------------- | ------------------------------------------------- |
| device           | device        | Name of the device that sent the reading          |
| temperature      | temperature   | Temperature value from the DHT22                  |
| humidity         | humidity      | Humidity value from the DHT22                     |
| uptime           | uptime        | Runtime value from the ESP32                      |
| MQTT topic       | topic         | Topic from which the message was received         |
| System time      | timestamp     | Time when the message was saved into the database |

Example saved database record:

```text
(18, 'ESP32-DHT22', 18, 27.9, 59.5, 65, 'iot/lab/group2', '2026-06-12 15:51:51')
```

This confirms that the data was successfully transferred from the physical sensor to the ESP32, published through MQTT, received by the PC, and stored in SQLite.

## ESP32 Firmware Setup

Before uploading the project files, the ESP32 was prepared by installing the required USB-to-serial drivers and flashing MicroPython firmware.

The ESP32 was detected on:

```text
COM8
```

To confirm communication with the ESP32, the following command was used:

```bash
python -m esptool --chip esp32 --port COM8 --baud 115200 chip-id
```

The ESP32 flash was then erased before installing the MicroPython firmware:

```bash
python -m esptool --chip esp32 --port COM8 erase_flash
```

The MicroPython firmware was written to the ESP32 using:

```bash
python -m esptool --chip esp32 --port COM8 --baud 460800 write_flash -z 0x1000 firmware/ESP32_GENERIC.bin
```

After flashing, Thonny IDE was configured to use MicroPython on ESP32 through the correct COM port.

## ESP32 Code Files

The ESP32 code is stored in the `esp32/` folder.

### `wifi.py`

This file handles WiFi connection. It stores the WiFi connection logic and allows the ESP32 to connect to a wireless network.

Main responsibility:

```text
ESP32 → WiFi Network → IP Address
```

### `mqtt_publish.py`

This file handles MQTT publishing. It connects the ESP32 to the MQTT broker and publishes sensor readings to the configured MQTT topic.

Main responsibility:

```text
ESP32 Sensor Data → JSON Payload → MQTT Broker
```

### `main.py`

This is the main MicroPython script that runs on the ESP32. It brings together the sensor reading, WiFi connection, and MQTT publishing logic.

Main responsibility:

```text
Read DHT22 → Connect WiFi → Publish MQTT Messages
```

## Subscriber Code Files

The PC-side code is stored in the `subscriber/` folder.

### `create_db.py`

Creates the SQLite database and required table for storing sensor readings.

### `subscriber.py`

Connects to the MQTT broker, subscribes to the topic `iot/lab/group2`, receives JSON messages, parses them, and inserts the data into SQLite.

Main responsibility:

```text
MQTT Broker → Python Subscriber → SQLite Database
```

### `view_data.py`

Displays saved sensor readings from the SQLite database.

### `export_db_data.py`

Exports stored database records into other readable formats such as CSV or Markdown.

### `sensor_data.db`

SQLite database file containing the saved sensor readings.

### `sensor_data_output.csv`

CSV export of the stored sensor data.

### `sensor_data_table.md`

Markdown table export of the stored sensor data.

## How to Run the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd IoT-Lab-ESP32-DHT22
```

### 2. Create and Activate a Python Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Required Python Package

```bash
pip install paho-mqtt
```

If `esptool` is not installed, install it using:

```bash
pip install esptool
```

### 4. Confirm ESP32 Connection

```bash
python -m esptool --chip esp32 --port COM8 --baud 115200 chip-id
```

Change `COM8` if your ESP32 appears on a different port.

### 5. Flash MicroPython Firmware

Erase the ESP32 flash:

```bash
python -m esptool --chip esp32 --port COM8 erase_flash
```

Write the MicroPython firmware:

```bash
python -m esptool --chip esp32 --port COM8 --baud 460800 write_flash -z 0x1000 firmware/ESP32_GENERIC.bin
```

### 6. Upload ESP32 Files using Thonny

Open Thonny IDE and configure the interpreter as:

```text
MicroPython (ESP32)
```

Then upload the files inside the `esp32/` folder to the ESP32:

```text
main.py
wifi.py
mqtt_publish.py
```

### 7. Create the SQLite Database

Navigate to the subscriber folder:

```bash
cd subscriber
```

Run:

```bash
python create_db.py
```

### 8. Run the Subscriber

In the same `subscriber/` folder, run:

```bash
python subscriber.py
```

The subscriber will connect to the MQTT broker and listen for messages on:

```text
iot/lab/group2
```

### 9. Run the ESP32 Program

Start or reset the ESP32 from Thonny. The ESP32 should read the DHT22 sensor and publish JSON messages through MQTT.

### 10. View Stored Data

After messages have been received, run:

```bash
python view_data.py
```

This will display the saved sensor readings from the SQLite database.

## Sample Output

Example database output:

```text
Saved sensor data:
----------------------------------------------------------------------------------------------------
(18, 'ESP32-DHT22', 18, 27.9, 59.5, 65, 'iot/lab/group2', '2026-06-12 15:51:51')
(17, 'ESP32-DHT22', 17, 27.9, 59.4, 61, 'iot/lab/group2', '2026-06-12 15:51:49')
(16, 'ESP32-DHT22', 16, 27.800002, 59.600004, 58, 'iot/lab/group2', '2026-06-12 15:51:45')
```

This output shows that the sensor readings were received and saved successfully.

## Screenshots and Evidence

The `screenshots/` folder contains evidence of each major stage of the lab:

| Screenshot                                            | Description                                 |
| ----------------------------------------------------- | ------------------------------------------- |
| `1a.Group-Image.jpeg`                                 | Group work evidence                         |
| `1b.Group-Image 2.jpeg`                               | Additional group evidence                   |
| `2a.Driver-Installation.png`                          | ESP32 driver installation                   |
| `2b.ESP32-Port-detected.png`                          | ESP32 detected on the correct COM port      |
| `3a.Confirming-ESP32-communication-with-computer.png` | ESP32 communication confirmed using esptool |
| `3b.Erasing-ESP32-flash.png`                          | ESP32 flash erase process                   |
| `3c.Writing-MicroPython-firmware-to-ESP32-flash.png`  | MicroPython firmware flashing               |
| `4a.Port-detected on thonny.png`                      | ESP32 port detected in Thonny               |
| `4b.Thonny-communicating-with-ESP32.png`              | Thonny communicating with ESP32             |
| `5a.Circuit-Connection1.png`                          | Circuit connection evidence                 |
| `5b.Circuit-Connection2.png`                          | Additional circuit connection evidence      |
| `6a.Saving-code-files-to-ESP32.png`                   | Uploading code files to ESP32               |
| `6b.Wifi-connected-successfully.png`                  | ESP32 connected to WiFi                     |
| `6c.Wifi-error.png`                                   | WiFi error encountered during testing       |
| `7.Testing-DHT22-sensor.png`                          | DHT22 sensor testing                        |
| `8a.MQTT-publishing.png`                              | MQTT publishing output                      |
| `8b.MQTT-subscribing.png`                             | MQTT subscriber receiving messages          |
| `9.Data-from-DB.png`                                  | SQLite database records                     |

## What the Project Demonstrates

This project demonstrates the following:

1. Correct wiring and integration of a DHT22 sensor with an ESP32.
2. ESP32 setup through driver installation, board detection, flash erasing, and MicroPython firmware installation.
3. Reading temperature and humidity values using MicroPython.
4. Connecting an ESP32 to a WiFi network.
5. Publishing structured JSON messages using MQTT.
6. Subscribing to MQTT messages from a PC using Python.
7. Saving IoT sensor readings into an SQLite database.
8. Verifying the system using REPL output, MQTT terminal output, and database records.

## Challenges Encountered

During implementation, the ESP32 initially required the correct USB-to-serial driver before it could be detected properly by the computer. This was resolved by installing the correct driver and confirming the COM port through Windows Device Manager.

Another issue involved confirming reliable communication with the ESP32 before flashing firmware. This was solved using the `chip-id` command in esptool, which confirmed that the board was connected and responding.

A WiFi connection issue was also encountered when the ESP32 did not connect immediately after the WiFi code was uploaded. The issue was resolved by pressing the ESP32 `RESET/EN` button, which restarted the board and allowed the MicroPython script to run again from the beginning. After the reset, the ESP32 connected successfully to the configured WiFi network and obtained an IP address.

The project also required careful DHT22 wiring. The 10 kΩ pull-up resistor was necessary to stabilize the data line and allow the sensor readings to be captured correctly.

MQTT testing also required correct topic matching and proper JSON formatting. The publisher and subscriber both had to use the same topic, `iot/lab/group2`, for successful communication.

## Conclusion

The project successfully implemented a complete IoT monitoring pipeline using ESP32, DHT22, MicroPython, MQTT, Python, and SQLite. The system collected live temperature and humidity data, transmitted it wirelessly through MQTT, received the messages on a PC, and stored the results in a local database.

The final implementation confirms that the system works from end to end, covering hardware integration, embedded programming, network communication, message publishing, subscription, and database persistence.
