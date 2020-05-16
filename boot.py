# This file is executed on every boot (including wake-boot from deepsleep)
try:
    import usocket as socket
except:
    import socket

import gc
import esp32
import network
import time  # check necessarity on boot
from machine import Pin, freq
from neopixel import NeoPixel

frequency = freq(240*10**6)  # 240 MHz Frequency

esp.osdebug(None)

gc.collect()
# import webrepl

# webrepl.start()

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PWD = "YOUR_WIFI_PASSWORD"

led = Pin(2, Pin.OUT)  # blue led on your ESP32 board
led.value(1)  # turn in on

LED_PIN = Pin(5, Pin.OUT)  # pin which your LED data wire connected to
LED_STRIP_LEN = 430  # amount of LEDs on your strip

# no one explains it but I will:
# bpp means bytes per pixel
# this value describes how many colors your LED strip have
led_strip = NeoPixel(LED_PIN, LED_STRIP_LEN, bpp=4)
