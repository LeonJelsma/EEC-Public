import socket

from MQTTT.SubscriberThread import SubscriberThread

subscriber = SubscriberThread()
subscriber.start()

while subscriber.is_alive():
    pass
