"""
Note that some variables used in this file are defined in boot.py
and both this files are read by ESP32 as one
"""


def strip_clear(strip):
    for i in range(LED_STRIP_LEN):
        led_strip[i] = (0, 0, 0, 0)
    strip.write()


def strip_fill_color(strip, red, green, blue, white):
    for i in range(LED_STRIP_LEN):
        led_strip[i] = (red, green, blue, white)
    strip.write()


def wifi_connect(wifi_ssid, wifi_pwd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_ssid, wifi_pwd)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def core_frequency_get():
    frequency = str(machine.freq()/10 ** 6)
    return 'Core frequency: ' + frequency + ' MHz'


def mcu_temperature_get():
    temp_c = str(round((esp32.raw_temperature() - 32) / 1.8, 1))
    return 'MCU temp: ' + temp_c + ' °C'


def wheel(pos):
    """
    Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r.
    """
    if pos < 0 or pos > 255:
        return 0, 0, 0, 0
    if pos < 85:
        return 255 - pos * 3, pos * 3, 0, 0
    if pos < 170:
        pos -= 85
        return 0, 255 - pos * 3, pos * 3, 0
    pos -= 170
    return pos * 3, 0, 255 - pos * 3, 0


def rainbow_cycle(wait=0):
    for j in range(255):
        for i in range(LED_STRIP_LEN):
            rc_index = (i * 256 // LED_STRIP_LEN) + j
            led_strip[i] = wheel(rc_index & 255)
        led_strip.write()
        if wait > 0:
            time.sleep_ms(wait)


def create_index_response(connection, filename='404.html', content_type='text/html'):
    if led.value() == 1:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"

    filesystem = os.listdir()
    if filename not in filesystem:
        error = 'Error: No ' + filename + ' file found in root dir. Found: ' + filesystem
        print(error)
        return error

    response = get_file(filename)
    response = response.format(
        gpio_state=gpio_state,
        frequency=core_frequency_get(),
        temperature=mcu_temperature_get(),
        dir_content=filesystem
    )
    connection.send('HTTP/1.1 200 OK\n')  # TODO write a cycle to send response page
    connection.send('Content-Type: ' + content_type + '\n')
    connection.send('Connection: close\n\n')
    connection.write(response)
    connection.close()


def get_file(filename):
    try:
        file = open(filename)
        html = file.read()
        file.close()
        return html
    except:
        return 'File not found'


def create_response(connection, filename='404.html', content_type='text/html'):
    response = get_file(filename)
    connection.send('HTTP/1.1 200 OK\n')  # TODO write a cycle to send response page
    connection.send('Content-Type: ' + content_type + '\n')
    connection.send('Connection: close\n\n')
    connection.write(response)
    connection.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


# SETUP
def setup():
    strip_clear(led_strip)
    wifi_connect(WIFI_SSID, WIFI_PWD)
    strip_fill_color(led_strip, 0, 0, 0, 255)


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
    if led_medium == 6:  # TODO wrap state check into separate function
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
    # TODO add color picker function
    if request.find('GET /style.css', 2, 17) >= 0:
        create_response(conn, 'style.css', 'text/css')
    elif request.find('GET /functions.js', 2, 20) >= 0:
        create_response(conn, 'functions.js', 'text/javascript')
    elif request.find('GET /?color=', 2, 19) >= 0:
        # TODO get colorsting into variable
        red_index = request.find('GET /?color=') + len('GET /?color=')
        green_index = red_index + 2
        blue_index = green_index + 2
        # TODO wrap this shit into functions
        red_val = int(request[red_index:green_index], 16)
        green_val = int(request[green_index:blue_index], 16)
        blue_val = int(request[blue_index:blue_index+2], 16)
        print(red_val)
        print(green_val)
        print(blue_val)
        # TODO send color values to LED strip
        create_index_response(conn, 'index.html', 'text/html')
    else:
        create_index_response(conn, 'index.html', 'text/html')
