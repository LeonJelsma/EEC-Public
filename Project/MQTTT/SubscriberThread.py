import json
import threading
from json import JSONDecodeError

import db_access
import paho.mqtt.client as mqtt
import requests

from MQTTT import util

API_SENSOR = "http://127.0.0.1:8000/api/sensors/"

SENSOR_TYPES = {
    'temperature': {'api': 'temperature_measurements/', 'parser': util.parse_temperature},
    'ambient': {'api': 'ambient_measurements/', 'parser': util.parse_ambient},
    'power': {'api': 'power_measurements/', 'parser': util.parse_power}
}


class SubscriberThread(threading.Thread):
    def __init__(self):

        self.mqttClient = mqtt.Client()
        self.mqttClient.on_message = self.on_message
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.tls_set(ca_certs='certs/ca.crt', certfile='certs/client.crt',
               keyfile='certs/client.key')
        self.mqttClient.connect(host="HOST", port=8883)
        self.mqttClient.subscribe("sensors/temperature")
        self.mqttClient.subscribe("sensors/ambient")
        self.mqttClient.subscribe("sensors/power")
        threading.Thread.__init__(self)

    def run(self):
        self.mqttClient.loop_forever()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    @staticmethod
    def on_message(_client, userdata, msg):
        url_fragment = ''
        try:
            message = json.loads(msg.payload)
        except JSONDecodeError as e:
            print('Could not decode message: ' + str(msg.payload))
            return
        for key, value in SENSOR_TYPES.items():
            if key in msg.topic:
                url_fragment = value['api']
                message = value['parser'](message, API_SENSOR)
                break
        if url_fragment == '':
            print('Invalid message received')
            return
        else:
            SubscriberThread.forward_measurement(url_fragment=url_fragment, message=message)

    @staticmethod
    def forward_measurement(url_fragment: str, message):
        server_address = "http://HUB:8000/api/"
        url = server_address + url_fragment
        response = requests.post(url=url, data=message)
        print('Request handled with statuscode: ' + str(response.status_code))
