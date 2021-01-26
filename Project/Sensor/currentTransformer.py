from ads1115 import ADS1115  # Importing the Adafruit ADS1115 library for Python
from machine import Pin, I2C  # Importing standard libraries of the ESP32
from math import sqrt
from time import time


class CurrentMeasurement():
    I2C_SCL = Pin(21)  # I2C ESP32 Clock pin to the ADS1115 Converter
    I2C_SDA = Pin(22)  # I2C ESP32 Data pin to the ADS1115 Converter
    I2C_FREQUENCY = 400000  # I2C Communication frequency
    I2C_ADDRESS = 0x48  # Standard I2C Address of the ADC Converter
    i2c = I2C(scl=I2C_SCL, sda=I2C_SDA, freq=I2C_FREQUENCY)
    # The following measurements are not static. These can change compared to the instruments you use.
    MULTIMETER = 0.2866  # Comparison measurement
    SCT013 = 0.346991945  # Comparison measurement
    ADJUST = MULTIMETER / SCT013
    # These values are static for the SCT-013 Current Transformer.
    FACTOR = 30  # 30 Amps per 1 Volt (30A/1V)
    GAIN = 4  # Gain setting of the ADS1115 ADC (1.024V)
    MULTIPLIER = (GAIN * 1.024) / 2 ** 16  # Transformation multiplier for the correct measurement.
    ADS = ADS1115(i2c, address=I2C_ADDRESS, gain=GAIN)
    SAMPLES = [0, 1, 2, 3, 4, 5, 6, 7]  # Selection for max samples per second.
    #          8, 16, 32, 64, 128, 250, 475, 860 Samples per second
    SAMPLES_SELECTED = 7
    CHANNEL = [0, 1]  # Comparison between channels (Standard = [0, None])
    FETCH_TIME = 1  # Run Fetch_Current while loop for # seconds
    WINDINGS = 1  # Amount of wire windings around the SCT-013 (Straigth through is 1)

    def measureVoltage(self, test=False):
        r"""
        There are two comparison classes in the library:
            read(rate=4, channel1=0, channel2=None)
                rate: The sample speed of the ADS1115 ADC
                channel1: Channel to measure
                channel2: If specified, the read function will compare channel1 with channel2

            set_conv(rate=4, channel1=0, channel2=None) and read_rev()
                rate: The sample speed of the ADS1115ADC
                channel1: Channel to measure
                channel2: If specified, the set_conv function will compare channel1 with channel2
            read_rev(): Used to read the value(s) of the configured channel(s) from set_conv()

        Some extra prototyping and testing is necessary for determining the best option.
        """

        # value = ADS.read(self.SAMPLES_SELECTED, self.CHANNEL[0], self.CHANNEL[1])
        self.ADS.set_conv(self.SAMPLES_SELECTED, self.CHANNEL[0], self.CHANNEL[1])
        value = self.ADS.read_rev()

        if value <= 5:
            value = 0

        if test == True:  # Optional. It will slow down execution time.
            print("ADC Measured: %s" % value)

        return value

    def Fetch_Current(self, test=[False, False]):
        total = 0.0
        counter = 0
        time_end = time() + self.FETCH_TIME

        # Fetch 'measurement' unlimited amount of time in set time limit.
        while time() < time_end:
            measurement = CurrentMeasurement().measureVoltage(
                test=test[1])  # Ensuring that the result of the measurement is absolute
            voltage = measurement * self.MULTIPLIER
            # voltage = (GAIN / 32767) * measurement
            current = voltage * self.FACTOR

            total += current
            counter += 1

        current = ((total / counter) / sqrt(2) * self.ADJUST) / self.WINDINGS
        if test[0] == True:
            print("Current: %s" % current)
            print("Count: %s" % counter)

        return current
