from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Room)
admin.site.register(Sensor)
admin.site.register(TempMeasurements)
admin.site.register(AmbientMeasurements)
admin.site.register(PowerMeasurements)
