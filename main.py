import network
import urequests as requests
import ujson
from time import sleep
from machine import Pin
import dht

# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBUS-M3UEAfRnBdKipvvZPAP9PZgd1epHbq"
DEVICE_LABEL = "esp32-11"
VARIABLE_LABEL1 = "temperature"
VARIABLE_LABEL2 = "humidity"

WIFI_SSID = "bunda"
WIFI_PASSWORD = "puanglette"

sensor = dht.DHT22(Pin(15))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Menghubungkan ke Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        while not wlan.isconnected():
            print("Menunggu koneksi...")
            sleep(1)

    print("Wi-Fi Connected!")
    print("IP Address:", wlan.ifconfig()[0])

def send_to_ubidots(variable_label, value):
    url = "https://industrial.api.ubidots.com/api/v1.6/devices/{}".format(DEVICE_LABEL)
    apiUrl = "http://192.168.1.12:5000/data"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": UBIDOTS_TOKEN
    }
    apiHeaders = {
        "Content-Type": "application/json",
    }
    data = {variable_label: value}
    try:
        response = requests.post(url, headers=headers, data=ujson.dumps(data))  # Ke Ubidots
        responseToApi = requests.post(apiUrl, headers=apiHeaders, data=ujson.dumps(data))  # Ke API lokal
        print("Response:", response.text)
        response.close()
        responseToApi.close()
    except Exception as e:
        print("Error:", e)
        print("URL:", url)
        print("Payload:", ujson.dumps(data))

prev_temp = None
prev_humidity = None

connect_wifi()

while True:
    print("Measuring weather conditions... ", end="")
    sensor.measure() 
    current_temp = sensor.temperature()
    current_humidity = sensor.humidity()

    if current_temp != prev_temp or current_humidity != prev_humidity:
        send_to_ubidots(VARIABLE_LABEL1, current_temp)
        send_to_ubidots(VARIABLE_LABEL2, current_humidity)
        prev_temp = current_temp
        prev_humidity = current_humidity
    else:
        print("No change")
    sleep(2)
