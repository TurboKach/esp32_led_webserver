
# This file is executed on every boot (including wake-boot from deepsleep)
try:
  import usocket as socket
except:
  import socket
  
from machine import Pin, freq
import network

freq(160*10**6) # 160 MHz Frequency

import esp

esp.osdebug(None)

import gc
gc.collect()
#import webrepl

#webrepl.start()

from neopixel import NeoPixel

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PWD = "YOUR_WIFI_PASSWORD"

led = Pin(2, Pin.OUT) # blue led on your esp32
led.value(1)

LED_PIN = Pin(5, Pin.OUT) # pin connected to your LED strip
led_strip_len = 430 # amount of LEDs on your strip

led_strip = NeoPixel(LED_PIN, led_strip_len)
