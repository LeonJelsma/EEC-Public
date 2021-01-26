import socket

import ujson
import machine
import mqtt
import sensor as sensor_
from state import State
from util import wifi_is_connected
import utime


class MqttClient:

    def __init__(self, sensor: sensor_.Sensor):
        self.sensor = sensor
        self.state = State()
        self.mqtt_client: mqtt.Client = None
        self.lost_connection = True
        self.type = self.state.get_value('type')

    def run(self):
        print("MQTT: Running")
        try:
            if wifi_is_connected():
                if self.lost_connection:
                    self.mqtt_client = mqtt.Client('HUB')
                    self.lost_connection = False
                    # try:
                print("MQTT: Attempting publish")
                measurement = self.sensor.get_measurement()
                message = {
                    'id': self.state.get_value('id'),
                    'measurement': measurement
                }
                print('Publishing temperature')
                self.mqtt_client.publish(topic='sensors/' + self.type, msg=ujson.dumps(message))
                utime.sleep_ms(1000)
            else:
                print("MQTT: No WiFi")
                self.lost_connection = True
        except Exception as e:
            print('MQTT Crashed: ' + str(e))
            return
