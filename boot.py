# This file is executed on every boot (including wake-boot from deepsleep)

# Here you can import your libraries and define constant variables

try:
    import usocket as socket
except:
    import socket

import gc
import esp
import esp32
import network
import os
import time  # check necessarity on boot
import machine
from neopixel import NeoPixel


MHZ = 10**6
FREQUENCY = 240 * MHZ
machine.freq(FREQUENCY)  # 240 MHz Frequency

esp.osdebug(None)

gc.collect()

WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PWD = os.getenv("WIFI_PWD")

board_led_blue = machine.Pin(2, machine.Pin.OUT)  # blue led on your ESP32 board

if WIFI_SSID is not None or WIFI_PWD is not None:
    board_led_blue.value(1)  # turn it on
else:
    print(
        "ERROR: Cannot get .env vars:\n" +
        "WIFI_SSID=" + str(WIFI_SSID) +
        "WIFI_PWD=" + str(WIFI_PWD)
    )


LED_PIN = machine.Pin(5, machine.Pin.OUT)  # pin which your LED data wire connected to. 5 = D5
LED_STRIP_LEN = 430  # amount of LEDs on your strip

DEFAULT_LED_STATE = (0, 0, 0, 255)  # default LED state is full white
CURRENT_LED_STATE = DEFAULT_LED_STATE

# no one explains it but I will:
# bpp means bytes per pixel
# this value describes how many colors your LED strip has
# example: RGB bpp=3, RGBW/RGBY bpp=4
led_strip = NeoPixel(LED_PIN, LED_STRIP_LEN, bpp=4)
