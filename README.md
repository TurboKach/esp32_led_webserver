# esp32_led_webserver
MicroPython ESP32 Web server for RGBW led strip control with color picker.

Hardware:
 - [ESP32-DevKit v1](https://www.espressif.com/en/products/devkits/esp32-devkitc/overview)
 - [RGBW LED strip](https://aliexpress.ru/item/32476317187.html)
 
 Software:
  - [esptool](https://github.com/espressif/esptool/)
  - ampy

Project architecture (read [MicroPython doc](http://docs.micropython.org/en/latest/esp32/quickref.html) for more):
 - [boot.py](https://github.com/TurboKach/esp32_led_webserver/blob/master/boot.py) - script is executed first (if it exists) 
 - [main.py](https://github.com/TurboKach/esp32_led_webserver/blob/master/main.py) - main script.  
 - index.html
 - functions.js
 - style.css