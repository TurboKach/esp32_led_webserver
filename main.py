"""
Note that some variables used in this file are defined in boot.py
and both this files are read by ESP32 as one
"""

# constants
NOT_FOUND_TEMPLATE = '404.html'
TEXT_HTML = 'text/html'
TEXT_CSS = 'text/css'
TEXT_JAVASCRIPT = 'text/javascript'


def strip_clear(strip):
    """
    Turns off all the strip LEDs
    :param strip: instance of NeoPixel led strip object (defined in `boot.py` as `led_strip` variable)
    :return: None
    """

    for i in range(LED_STRIP_LEN):
        led_strip[i] = (0, 0, 0, 0)  # R G B W

    strip.write()


def strip_fill_color(strip=None, red=0, green=0, blue=0, white=0):
    """
    Fill all strip LEDs with defined colors
    This function is useful for setting the same color to the whole strip

    :param strip: instance of NeoPixel led strip object (defined in `boot.py` as `led_strip` variable)
    :param red: RED color value (0-255)
    :param green: GREEN color value (0-255)
    :param blue: BLUE color value (0-255)
    :param white: WHITE color value (0-255)
    :return: None
    """
    if strip is None:
        strip = NeoPixel(LED_PIN, LED_STRIP_LEN, bpp=4)

    for i in range(LED_STRIP_LEN):
        led_strip[i] = (red, green, blue, white)

    strip.write()


def wifi_connect(wifi_ssid=None, wifi_pwd=''):
    """
    Connects your ESP32 to chosen Wi-Fi access point untill success (loop otherwise)

    :param wifi_ssid: access point SSID
    :param wifi_pwd: access point password
    :return: None
    """
    if wifi_ssid is None:
        raise ConnectionError('No Wi-Fi SSID provided. Check your settings.')

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_ssid, wifi_pwd)
        if not wlan.isconnected():
            print('retrying...')
            time.sleep_ms(2000)

    print('Connected.\nNetwork config: \n', wlan.ifconfig())


def core_frequency_get():
    """
    Retrieve set core frequency
    :return: string message with frequency in MHz
    """
    frequency = str(machine.freq() / MHZ)
    return 'Core frequency: ' + frequency + ' MHz'


def mcu_temperature_get():
    """
    Retreive current core temperature
    :return: string message with temperature in Celsius
    """
    temp_c = str(round((esp32.raw_temperature() - 32) / 1.8, 1))
    return 'MCU temp: ' + temp_c + ' °C'


def wheel(pos):
    """
    Wheel is a width of a single rainbow line

    Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r.
    """
    if pos < 0 or pos > 255:
        return 0, 0, 0, 0
    if pos < 85:
        # TODO add incoming commands check while spinning rainbow wheel
        return 255 - pos * 3, pos * 3, 0, 0
    if pos < 170:
        pos -= 85
        return 0, 255 - pos * 3, pos * 3, 0
    pos -= 170
    return pos * 3, 0, 255 - pos * 3, 0


def rainbow_cycle(wait=0):
    for j in range(256):
        for i in range(LED_STRIP_LEN):
            rc_index = (i * 256 // LED_STRIP_LEN) + j
            led_strip[i] = wheel(rc_index & 255)
        led_strip.write()
        if wait > 0:
            time.sleep_ms(wait)  # change to remove sleep


def create_response(connection, filename=NOT_FOUND_TEMPLATE, content_type=TEXT_HTML):
    response = get_file(filename)
    connection.send('HTTP/1.1 200 OK\n')  # TODO write a cycle to send response page
    connection.send('Content-Type: ' + content_type + '\n')
    connection.send('Connection: close\n\n')
    connection.write(response)
    connection.close()


def create_index_response(connection, filename=NOT_FOUND_TEMPLATE, content_type=TEXT_HTML):
    if led.value() == 1:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"

    response = get_file(filename)
    response = response.format(
        gpio_state=gpio_state,
        frequency=core_frequency_get(),
        temperature=mcu_temperature_get(),
        dir_content=os.listdir()
    )
    connection.send('HTTP/1.1 200 OK\n')  # TODO write a cycle to send response page
    connection.send('Content-Type: ' + content_type + '\n')
    connection.send('Connection: close\n\n')
    connection.write(response)
    connection.close()


def get_file(filename):
    """
    Returns a file from ESP32 filesystem
    :param filename:
    :return:
    """
    try:
        filesystem = os.listdir()
        if filename not in filesystem:
            error = 'Error: ' + filename + ' file not found in root dir. Found: ' + filesystem
            print(error)
            return error  # TODO check it is safe to return a string instead of file
        file = open(filename)
        f = file.read()
        file.close()
        return f
    except Exception as e:
        return e


def color_read(request):
    color_request = 'GET /?color='
    red_index = request.find(color_request) + len(color_request)
    green_index = red_index + 2
    blue_index = green_index + 2
    # TODO wrap this shit into functions
    red_val = int(request[red_index:green_index], 16)
    green_val = int(request[green_index:blue_index], 16)
    blue_val = int(request[blue_index:blue_index + 2], 16)

    return red_val, green_val, blue_val


def setup():
    """
    1. Clears an LED strip
    2. Connects to Wi-Fi
    3. Fills a strip with warm white color at a max brightness

    :return: None
    """
    strip_clear(led_strip)
    wifi_connect(WIFI_SSID, WIFI_PWD)  # this constants defined at boot.py
    strip_fill_color(led_strip, *DEFAULT_LED_STATE)


# ========= SETUP AND RUN =========

# open a socket on port 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

setup()

# ========= INFINITE LOOP =========
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
        led.value(1)
        strip_fill_color(led_strip, 0, 0, 0, 150)
    if led_low == 6:
        print('LED LOW')
        led.value(1)
        strip_fill_color(led_strip, 0, 0, 0, 50)
    if led_on == 6:
        print('LED ON')
        led.value(1)
        strip_fill_color(led_strip, 0, 0, 0, 255)
    if led_off == 6:
        print('LED OFF')
        led.value(0)
        strip_clear(led_strip)
    if led_rainbow == 6:
        print('RAINBOW MODE')
        led.value(1)
        rainbow_cycle()
    # TODO add color picker function
    # TODO keep .css and .js files on external server to reduce requests on ESP32 (requires internet access)
    if request.find('GET /style.css', 2, 17) >= 0:
        create_response(conn, 'style.css', TEXT_CSS)
    elif request.find('GET /functions.js', 2, 20) >= 0:
        create_response(conn, 'functions.js', TEXT_JAVASCRIPT)
    elif request.find('GET /?color=', 2, 19) >= 0:
        # TODO get colorsting into variable
        rgb = color_read(request)

        strip_fill_color(led_strip, *rgb)

    create_index_response(conn, 'index.html', TEXT_HTML)
