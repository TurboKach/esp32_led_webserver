# esp32_led_webserver
MicroPython ESP32 Web server for RGBW led strip control with color picker.

Hardware:
 - [ESP32-DevKit v1](https://www.espressif.com/en/products/devkits/esp32-devkitc/overview)
 - [RGBW LED strip](https://aliexpress.ru/item/32476317187.html)
 
 Software:
  - [esptool](https://github.com/espressif/esptool/)
  - [ampy](https://github.com/scientifichackers/ampy)

Project architecture (read [MicroPython doc](http://docs.micropython.org/en/latest/esp32/quickref.html) for more):
 - [boot.py](https://github.com/TurboKach/esp32_led_webserver/blob/master/boot.py) - script is executed first (if it exists) 
 - [main.py](https://github.com/TurboKach/esp32_led_webserver/blob/master/main.py) - main script.  
 - index.html
 - functions.js
 - style.css
 
 ####Step-by-step guide
 0. You might need to install [CP210x USB to UART bridge driver](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
1. Get the latest stable MicroPython [firmware](https://micropython.org/download/esp32/)  or take mine
2. Install [esptool](https://github.com/espressif/esptool)
3. Erase flash with esptool: `esptool.py --port /dev/cu.usbserial-0001 erase_flash`  
4. Deploy firmware : `esptool.py --chip esp32 --port /dev/cu.usbserial-0001 write_flash -z 0x1000 esp32-idf3-20200902-v1.13.bin
`  
5. Load project files to the board using [ampy](https://github.com/scientifichackers/ampy) (from project directory):  
`ampy -p /dev/cu.usbserial-0001 put boot.py`  
`ampy -p /dev/cu.usbserial-0001 put main.py`  
`ampy -p /dev/cu.usbserial-0001 put index.html`  
`ampy -p /dev/cu.usbserial-0001 put functions.js`  
`ampy -p /dev/cu.usbserial-0001 put style.css`  
6. Check it works by visiting ESP32 IP address  
7. **TO BE CONTINUED**
