import uuid

from django.shortcuts import render
from rest_framework import viewsets

from .serializers import *
from .models import *


# Create your views here.

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('name')
    serializer_class = RoomSerializer


class SensorViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        room_id = self.request.query_params.get('room_id')
        if room_id:
            return Sensor.objects.all().filter(room=room_id)
        return Sensor.objects.all()

    queryset = Sensor.objects.all().order_by('room')
    serializer_class = SensorSerializer


class TempMeasurementViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        sensor_id = self.request.query_params.get('sensor_id')
        if sensor_id:
            return TempMeasurements.objects.all().filter(sensor=sensor_id)
        return TempMeasurements.objects.all()

    queryset = TempMeasurements.objects.all().order_by('sensor')
    serializer_class = TempMeasurementsSerializer


class AmbientMeasurementViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        sensor_id = self.request.query_params.get('sensor_id')
        if sensor_id:
            return AmbientMeasurements.objects.all().filter(sensor=sensor_id)
        return AmbientMeasurements.objects.all()

    queryset = AmbientMeasurements.objects.all().order_by('sensor')
    serializer_class = PowerMeasurementsSerializer


class PowerMeasurementViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        sensor_id = self.request.query_params.get('sensor_id')
        if sensor_id:
            return PowerMeasurements.objects.all().filter(sensor=sensor_id)
        return PowerMeasurements.objects.all()

    queryset = PowerMeasurements.objects.all().order_by('sensor')
    serializer_class = PowerMeasurementsSerializer
