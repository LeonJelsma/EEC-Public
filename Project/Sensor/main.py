import network
import machine
import _thread
import utime
import sensor
import util
from webserver import WebServer
from mqttclient import MqttClient
from state import State

try:
    import usocket as socket
except ModuleNotFoundError:
    import socket

state = State()
# Configuration
state.save_value(key='id', value=1)
state.save_value(key='type', value='temperature')

webserver = WebServer()
#webserver.start()
webThread = _thread.start_new_thread(webserver.start, ())

type = state.get_value('type')
if type == 'temperature':
    sensor = sensor.TemperatureSensor()
elif type == 'power':
    sensor = sensor.PowerSensor()
elif type == 'ambient':
    sensor = sensor.AmbientSensor()

webserver.router.set_sensor(sensor)

mqttClient = MqttClient(sensor=sensor)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

if not state.is_configured():
    print('Sensor not configured')

# Main loop
publish_delay = 500
check_server_delay = 100
last_publish = utime.ticks_ms()
print('entering main loop')
while True:
    if not util.wifi_is_connected():
        if state.is_configured():
            print(state.get_value('SSiD') + '--' + state.get_value('password'))
            util.connect_to_network(state.get_value('SSiD'), state.get_value('password'))
    if utime.ticks_diff(utime.ticks_ms(), last_publish) > publish_delay:
        mqttClient.run()
        last_publish = utime.ticks_ms()
    #if utime.ticks_diff(utime.ticks_ms(), last_publish) > publish_delay:
        #webserver.run()
