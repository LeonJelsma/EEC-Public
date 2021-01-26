from datetime import date, timedelta, datetime
from api.models import TempMeasurements, AmbientMeasurements, PowerMeasurements, Sensor, Room, SensorType

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg
from django.db.models.functions import TruncMinute

from pprint import pprint


class Command(BaseCommand):
    help = 'Aggregate the database'

    def handle(self, *args, **kwargs):
        yesterday = date.today()  # - timedelta(days=1)
        # temp
        temp_past_day = TempMeasurements.objects.filter(
            timestamp__year=yesterday.year,
            timestamp__month=yesterday.month,
            timestamp__day=yesterday.day)

        test = temp_past_day.annotate(timemin=TruncMinute('timestamp')).values(
            'timemin', 'sensor').annotate(avg_temp=Avg('temperature'))

        temp_past_day.delete()

        for t in test:
            TempMeasurements.objects.create(
                temperature=t['avg_temp'],
                sensor=Sensor.objects.get(id=t['sensor']),
                timestamp=t['timemin']
            )

        # ambient
        amb_past_day = AmbientMeasurements.objects.filter(
            timestamp__year=yesterday.year,
            timestamp__month=yesterday.month,
            timestamp__day=yesterday.day)

        test = amb_past_day.annotate(timemin=TruncMinute('timestamp')).values('timemin', 'sensor').annotate(
            avg_temp=Avg('temperature'),
            avg_ppm=Avg('air_quality'),
            avg_hum=Avg('humidity')
        )

        amb_past_day.delete()

        for t in test:
            AmbientMeasurements.objects.create(
                air_quality=t['air_quality'],
                temperature=t['avg_temp'],
                humidity=t['humidity'],
                sensor=Sensor.objects.get(id=t['sensor']),
                timestamp=t['timemin']
            )

        # power
        pow_past_day = PowerMeasurements.objects.filter(
            timestamp__year=yesterday.year,
            timestamp__month=yesterday.month,
            timestamp__day=yesterday.day)

        test = pow_past_day.annotate(timemin=TruncMinute('timestamp')).values(
            'timemin', 'sensor').annotate(avg_temp=Avg('wattage'))

        pow_past_day.delete()

        for t in test:
            PowerMeasurements.objects.create(
                wattage=t['wattage'],
                sensor=Sensor.objects.get(id=t['sensor']),
                timestamp=t['timemin']
            )

    print('aggregated the database')
