from rest_framework import routers
from django.urls import path, include
from api import views
from .api import (
    UserCustomViewSet,
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

router.register('user', UserCustomViewSet, 'UserCustom')
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
    path('users/list', views.ListUsersView.as_view(), name='ListUsers'),
    # path(
    #    'create_superuser/', views.CreateSuperuserView.as_view(), name='CreateSuperuser'
    # ),
    # path('update_user/', views.UpdateSuperuserView.as_view(), name='UpdateSuperuser'),
    path('passenger/home/', views.home_passenger, name='HomePassenger'),
    path('passenger/register/', views.passenger_register, name='RegisterPassenger'),
    path('', include(router.urls)),
]
