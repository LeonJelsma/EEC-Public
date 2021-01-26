import uuid

from django.db import models

# Create your models here.
from django.utils import timezone
from django_enumfield import enum


class SensorType(enum.Enum):
    TEMPERATURE = 1
    AMBIENT = 2
    POWER = 3

    __labels__ = {
        TEMPERATURE: "Temperature sensor",
        AMBIENT: "Ambient sensor",
        POWER: "Power sensor"
    }


class Room(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = enum.EnumField(SensorType)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    activated = models.BooleanField()
    key = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name + ': ' + str(self.type)


class TempMeasurements(models.Model):
    temperature = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(editable=False, default=timezone.now)



class AmbientMeasurements(models.Model):
    air_quality = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return "%f %f %f" % (self.air_quality, self.temperature, self.humidity)


class PowerMeasurements(models.Model):
    wattage = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return self.wattage
