from rest_framework import routers
from django.urls import path, include
from api import views
from .api import (
    UsersViewSet,
    DriverViewSet,
    PassengerViewSet,
    VehicleColorViewSet,
    VehicleBrandViewSet,
    VehicleTypeViewSet,
    VehicleModelViewSet,
    VehicleViewSet,
    Driver_VehicleViewSet,
    TripViewSet,
    Passenger_TripViewSet,
)

router = routers.DefaultRouter()

router.register('Users', UsersViewSet, 'Users')
router.register('Driver', DriverViewSet, 'Driver')
router.register('Passenger', PassengerViewSet, 'Passenger')
router.register('VehicleColor', VehicleColorViewSet, 'VehicleColor')
router.register('VehicleBrand', VehicleBrandViewSet, 'VehicleBrand')
router.register('VehicleType', VehicleTypeViewSet, 'VehicleType')
router.register('VehicleModel', VehicleModelViewSet, 'VehicleModel')
router.register('Vehicle', VehicleViewSet, 'Vehicle')
router.register('Driver_Vehicle', Driver_VehicleViewSet, 'Driver_Vehicle')
router.register('Trip', TripViewSet, 'Trip')
router.register('Passenger_Trip', Passenger_TripViewSet, 'Passenger_Trip')

urlpatterns = [
    path('', include(router.urls)),
    path('ListUsers', views.ListUsersView.as_view(), name='ListUsers'),
    path('HomePassenger', views.home_passenger, name='HomePassenger'),
]
