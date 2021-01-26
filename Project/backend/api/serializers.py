from rest_framework import serializers

from .models import *


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = 'name', 'id'


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensor
        fields = 'name', 'room', 'activated', 'type', 'key', 'id'


class TempMeasurementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TempMeasurements
        fields = 'temperature', 'sensor', 'timestamp'


class PowerMeasurementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PowerMeasurements
        fields = 'wattage', 'sensor', 'timestamp'


class AmbientMeasurementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AmbientMeasurements
        fields = 'air_quality', 'temperature', 'humidity', 'sensor', 'timestamp'
