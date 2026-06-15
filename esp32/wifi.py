import network
import time

SSID = "bk"
PASSWORD = "12345678"


def connect_wifi():
    """
    Connect ESP32 to WiFi with a clean WiFi reset first.
    """

    wlan = network.WLAN(network.STA_IF)

    # Fully reset WiFi interface before connecting
    wlan.active(False)
    time.sleep(1)

    wlan.active(True)
    time.sleep(1)

    if wlan.isconnected():
        print("Already connected to WiFi")
        print("Network config:", wlan.ifconfig())
        return wlan

    print("Scanning for WiFi networks...")
    networks = wlan.scan()

    found = False
    for net in networks:
        name = net[0].decode()
        print("Found:", name)
        if name == SSID:
            found = True

    if not found:
        raise RuntimeError("WiFi network not found. Check hotspot name or use 2.4GHz.")

    print("Connecting to WiFi:", SSID)
    wlan.connect(SSID, PASSWORD)

    timeout = 30

    while not wlan.isconnected() and timeout > 0:
        print("Waiting for WiFi connection...")
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("WiFi connected successfully")
        print("Network config:", wlan.ifconfig())
        print("ESP32 IP address:", wlan.ifconfig()[0])
        return wlan

    raise RuntimeError("WiFi connection failed. Check password, hotspot band, or hotspot security.")
