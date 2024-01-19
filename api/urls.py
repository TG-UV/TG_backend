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

router.register('api/Driver', DriverViewSet, 'Driver')
router.register('api/Passenger', PassengerViewSet, 'Passenger')
router.register('api/VehicleColor', VehicleColorViewSet, 'VehicleColor')
router.register('api/VehicleBrand', VehicleBrandViewSet, 'VehicleBrand')
router.register('api/VehicleType', VehicleTypeViewSet, 'VehicleType')
router.register('api/VehicleModel', VehicleModelViewSet, 'VehicleModel')
router.register('api/Vehicle', VehicleViewSet, 'Vehicle')
router.register('api/Driver_Vehicle', Driver_VehicleViewSet, 'Driver_Vehicle')
router.register('api/Trip', TripViewSet, 'Trip')
router.register('api/PassangerTrip', PassangerTripViewSet, 'PassangerTrip')

urlpatterns = [
    path('', include(router.urls)),
    path('hello', views.hello_view, name='hello'),
    ##path('api/signin', views.signin)
]
