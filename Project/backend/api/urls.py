from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'sensors', views.SensorViewSet)
router.register(r'temperature_measurements', views.TempMeasurementViewSet)
router.register(r'ambient_measurements', views.PowerMeasurementViewSet)
router.register(r'power_measurements', views.AmbientMeasurementViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]