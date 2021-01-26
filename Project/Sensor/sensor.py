from mq135 import MQ135
from machine import Pin, I2C
from BME280 import BME280
from currentTransformer import CurrentMeasurement as cm


class Sensor:

    def __init__(self):
        super().__init__()

    def get_measurement(self):
        pass


class AmbientSensor(Sensor):

    def __init__(self):
        super().__init__()
        self.i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
        self.mq135 = MQ135(Pin(36))
        self.bme = BME280(i2c=self.i2c)

    def get_measurement(self):
        temp, hum, pres = self.bme.read()
        ppm = self.mq135.get_corrected_ppm_average(temp, hum)
        return {('temperature', 'humidity', 'pressure', 'ppm')[i]: v for i, v in enumerate((temp, hum, pres, ppm))}


class TemperatureSensor(Sensor):

    def __init__(self):
        super().__init__()
        self.i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
        self.bme = BME280(i2c=self.i2c)

    def get_measurement(self):
        return {('temperature', 'humidity', 'pressure')[i]: v for i, v in enumerate(self.bme.read())}


class PowerSensor(Sensor):

    def __init__(self):
        super().__init__()
        self.TEST_Fetch_Current = True  # Enable print function in CM().Fetch_Current
        self.TEST_measureVoltage = False  # Enable print function in CM().measureVoltage
        self.cm = cm()

    def get_measurement(self):
        return self.cm.Fetch_Current(test=[self.TEST_Fetch_Current, self.TEST_measureVoltage])