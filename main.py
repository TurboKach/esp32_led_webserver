def strip_clear(strip):
  for i in range(led_strip_len):
    led_strip[i] = (0, 0, 0, 0)
  strip.write()
  
def strip_fill_color(strip, red, green, blue, white):
  for i in range(led_strip_len):
    led_strip[i] = (red, green, blue, white)
  strip.write()


def wifi_connect(wifi_ssid, wifi_pwd):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PWD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

  
def get_freq():
  print("Frequency: " + str(int(freq())/1000000) + " MHz")
 
def get_mcu_temp():
  temp_c = round((esp32.raw_temperature()-32)/1.8, 1)
  print("MCU temp: " + str(temp_c) + " 掳C")  
  
def wheel(pos): 
  '''Input a value 0 to 255 to get a color value.
  The colours are a transition r - g - b - back to r.'''
  if pos < 0 or pos > 255:
    return (0, 0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3, 0)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3, 0)
  
def rainbow_cycle(wait=0):
  for j in range(255):
    for i in range(led_strip_len):
      rc_index = (i * 256 // led_strip_len) + j
      led_strip[i] = wheel(rc_index & 255)
    led_strip.write()
    if wait > 0:
      time.sleep_ms(wait)




def web_page():
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  html = """<html><head> <title>ESP32 LED</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: "SF Pro Display","SF Pro Icons","Helvetica Neue","Helvetica","Arial",sans-serif; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #000000; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #000000; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #000000;}</style></head><body> <h1>ESP32 WEB SERVER</h1> 
  <p>STATUS: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a><a href="/?led=off"><button class="button">OFF</button></a></p><p><a href="/?led=medium"><button class="button">Medium</button></a><a href="/?led=low"><button class="button">Low</button></a></p><a href="/?led=rainbow"><button class="button">RAINBOW</button></a>
  <p><input style="width: 100px; height: 50px;" type="color" value="#ff0000" /></p>
  <!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jscolor/2.0.4/jscolor.min.js"></script>
</head><body><div class="container"><div class="row"><h1>ESP Color Picker</h1></div>
<a class="btn btn-primary btn-lg" href="#" id="change_color" role="button">Change Color</a> 
<input class="jscolor {onFineChange:'update(this)'}" id="rgb"></div>
<script>function update(picker) {document.getElementById('rgb').innerHTML = Math.round(picker.rgb[0]) + ', ' +  Math.round(picker.rgb[1]) + ', ' + Math.round(picker.rgb[2]);
document.getElementById("change_color").href="?r" + Math.round(picker.rgb[0]) + "g" +  Math.round(picker.rgb[1]) + "b" + Math.round(picker.rgb[2]) + "&";}</script></body></html>
"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# SETUP
def setup():
  strip_clear(led_strip)
  wifi_connect(WIFI_SSID, WIFI_PWD)
  strip_fill_color(led_strip, 0, 0, 0,255)
    
setup()

# LOOP   
while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  led_rainbow = request.find('/?led=rainbow')
  led_medium = request.find('/?led=medium')
  led_low = request.find('/?led=low')
  if led_medium == 6:
    print('LED MEDIUM')
    strip_fill_color(led_strip, 0, 0, 0, 150)
    led_strip.write()
    led.value(1)
  if led_low == 6:
    print('LED LOW')
    strip_fill_color(led_strip, 0, 0, 0, 50)
    led_strip.write()
    led.value(1)
  if led_on == 6:
    print('LED ON')
    strip_fill_color(led_strip, 0, 0, 0, 255)
    led_strip.write()
    led.value(1)
  if led_off == 6:
    print('LED OFF')
    strip_clear(led_strip)
    led.value(0)
  if led_rainbow == 6:
    print('RAINBOW MODE')
    rainbow_cycle()
    led.value(1)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
  
  
