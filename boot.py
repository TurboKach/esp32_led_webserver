
# This file is executed on every boot (including wake-boot from deepsleep)
try:
  import usocket as socket
except:
  import socket
  
from machine import Pin, freq
import network

freq(160*1000000)

import esp

esp.osdebug(None)

import gc
gc.collect()
#import webrepl

#webrepl.start()

from neopixel import NeoPixel

WIFI_SSID = "RT-WiFi-0C8B"
WIFI_PWD = "2829001335"

led = Pin(2, Pin.OUT)
led.value(1)

LED_PIN = Pin(5, Pin.OUT)
led_strip_len = 430

led_strip = NeoPixel(LED_PIN, led_strip_len)
