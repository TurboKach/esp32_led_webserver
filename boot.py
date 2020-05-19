# This file is executed on every boot (including wake-boot from deepsleep)
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

machine.freq(240*10**6)  # 240 MHz Frequency

esp.osdebug(None)

gc.collect()
# import webrepl

# webrepl.start()

WIFI_SSID = "Wireless Lab"
WIFI_PWD = "manowawafli"

led = machine.Pin(2, machine.Pin.OUT)  # blue led on your ESP32 board
led.value(1)  # turn in on

LED_PIN = machine.Pin(5, machine.Pin.OUT)  # pin which your LED data wire connected to
LED_STRIP_LEN = 430  # amount of LEDs on your strip

# no one explains it but I will:
# bpp means bytes per pixel
# this value describes how many colors your LED strip have
led_strip = NeoPixel(LED_PIN, LED_STRIP_LEN, bpp=4)
