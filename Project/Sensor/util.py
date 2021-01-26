import network
import utime


def scan_networks():
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    networks = nic.scan()
    nic.active(False)
    return networks


def start_ap(name='EEC-Sensor'):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=name)
    while not ap.active():
        pass
    print('AP Started')


def wifi_is_connected():
    sta_if = network.WLAN(network.STA_IF)
    return sta_if.isconnected()


def connect_to_network(ssid=None, password=None):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if sta_if.isconnected():
        sta_if.disconnect()
    sta_if.connect(ssid, password)
    print('connecting to network...')
    timeout = 5000
    start = utime.ticks_ms()
    while not sta_if.isconnected():
        if utime.ticks_diff(utime.ticks_ms(), start) > timeout:
            print('Connecting to WiFi timed out')
            break
