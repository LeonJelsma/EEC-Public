import json
import random
from time import sleep
import time

import paho.mqtt.client as mqtt
import requests
import concurrent.futures


def get_client():
    client = mqtt.Client()
    client.tls_set(ca_certs='certs/ca.crt', certfile='certs/client.crt',
                   keyfile='certs/client.key')
    client.connect('HOST', 8883)
    return client
    client.publish(topic='test', payload='TEST')


def generate_sensors(count):
    base_name = "tempsensor"
    room = "http://HUB:8000/api/rooms/1/"
    for i in range(count):
        url = "http://HUB:8000/api/sensors/"
        message = {
            "name": base_name + str(i),
            "room": room,
            "activated": True,
            "type": 1
        }
        response = requests.post(url=url, data=message)
        print('Request handled with statuscode: ' + str(response.status_code))


def get_sensors():
    url = "http://HUB:8000/api/sensors/"
    response = json.loads(requests.get(url=url).text)
    return response


def add_measurements(sensors):
    url = "http://HUB:8000/api/temperature_measurements/"
    for sensor in sensors:
        message = {
            "id": sensor["id"],
            "measurement": {
                "temperature": random.randint(10, 20),
            }
        }
        response = requests.post(url, )


def do_load_test():
    sensors = get_sensors()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for sensor in sensors:
            futures.append(executor.submit(publish_measurements, sensor, 100))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


def publish_measurements(sensor, count):
    start_time = time.time()
    index = 0
    client = get_client()
    while index < count:
        sleep(1)
        index += 1
        message = {
            "id": sensor["id"],
            "measurement": {
                "temperature": random.randint(10, 20),
            }
        }
        client.publish(topic='sensors/temperature', payload=json.dumps(message))
        end_time = time.time()
        print("Sensor: " + str(sensor["id"]) + " published message #" + str(index) + " at " + str(
            round(end_time - start_time, 3)) + " seconds\n")
    return str(sensor["id"]) + " is done"


do_load_test()
