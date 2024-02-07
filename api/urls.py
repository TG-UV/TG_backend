from rest_framework import routers
from django.urls import path, include
from api import views
from .api import (
    SuperuserViewSet,
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

router.register('superuser', SuperuserViewSet, 'Superuser')
router.register('driver', DriverViewSet, 'Driver')
router.register('passenger', PassengerViewSet, 'Passenger')
router.register('vehicleColor', VehicleColorViewSet, 'VehicleColor')
router.register('vehicleBrand', VehicleBrandViewSet, 'VehicleBrand')
router.register('vehicleType', VehicleTypeViewSet, 'VehicleType')
router.register('vehicleModel', VehicleModelViewSet, 'VehicleModel')
router.register('vehicle', VehicleViewSet, 'Vehicle')
router.register('driver_vehicle', Driver_VehicleViewSet, 'Driver_Vehicle')
router.register('trip', TripViewSet, 'Trip')
router.register('passenger_trip', Passenger_TripViewSet, 'Passenger_Trip')

urlpatterns = [
    path('', include(router.urls)),
    path('list_users/', views.ListUsersView.as_view(), name='ListUsers'),
    path('home_passenger/', views.home_passenger, name='HomePassenger'),
    path(
        'create_superuser/', views.CreateSuperuserView.as_view(), name='CreateSuperuser'
    ),
    path(
        'update_superuser/', views.UpdateSuperuserView.as_view(), name='UpdateSuperuser'
    ),
]
