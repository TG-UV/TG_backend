from rest_framework import routers
from django.urls import path, include
from api import views
from .api import (
    DriverViewSet,
    PassengerViewSet,
    VehicleColorViewSet,
    VehicleBrandViewSet,
    VehicleTypeViewSet,
    VehicleModelViewSet,
    VehicleViewSet,
    Driver_VehicleViewSet,
    TripViewSet,
    PassangerTripViewSet,
)

router = routers.DefaultRouter()

router.register('Driver', DriverViewSet, 'Driver')
router.register('Passenger', PassengerViewSet, 'Passenger')
router.register('VehicleColor', VehicleColorViewSet, 'VehicleColor')
router.register('VehicleBrand', VehicleBrandViewSet, 'VehicleBrand')
router.register('VehicleType', VehicleTypeViewSet, 'VehicleType')
router.register('VehicleModel', VehicleModelViewSet, 'VehicleModel')
router.register('Vehicle', VehicleViewSet, 'Vehicle')
router.register('Driver_Vehicle', Driver_VehicleViewSet, 'Driver_Vehicle')
router.register('Trip', TripViewSet, 'Trip')
router.register('PassangerTrip', PassangerTripViewSet, 'PassangerTrip')

urlpatterns = [
    path('', include(router.urls)),
    path('hello', views.hello_view, name='hello'),
    ##path('api/signin', views.signin)
]
