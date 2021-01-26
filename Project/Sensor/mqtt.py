import ubinascii
from machine import unique_id
from mqttsimple import MQTTClient


class Client():
    def __init__(self, mqtt_server, key=None, crt=None, auto_reconnect=True):
        self.client_id = ubinascii.hexlify(unique_id())
        self.mqtt_server = mqtt_server
        self.auto_reconnect = auto_reconnect

        if key and crt:
            with open(key, 'r') as f:
                self.key = f.read()
            with open(crt, 'r') as f:
                self.crt = f.read()
        else:
            self.key = self.crt = None

        self.connect()

    def connect(self):
        self.client = MQTTClient(
            self.client_id,
            self.mqtt_server,
            ssl=self.key and self.crt,
            ssl_params={'cert': self.crt, 'key': self.key} if self.key and self.crt else {}
        )
        self.client.connect()

    def publish(self, topic, msg):
        try:
            self.client.publish(topic, msg)
        except OSError as e:
            if self.auto_reconnect:
                self.connect()
