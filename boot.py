# This file is executed on every boot (including wake-boot from deepsleep)
try:
  import usocket as socket
except:
  import socket
  
from machine import Pin, freq
import network

freq(240*10**6) # 240 MHz Frequency

import esp

esp.osdebug(None)

import gc
gc.collect()
#import webrepl

#webrepl.start()

from neopixel import NeoPixel

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PWD = "YOUR_WIFI_PASSWORD"

led = Pin(2, Pin.OUT)
led.value(1)

LED_PIN = Pin(5, Pin.OUT)
led_strip_len = 430

# no one explains it but I will:
# bpp means bytes per pixel
# this value describes how many colors your LED strip have
led_strip = NeoPixel(LED_PIN, led_strip_len, bpp=4)
