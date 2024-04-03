from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from api import views
from .api import (
    ExtendedUserViewSet,
    UserTypeViewSet,
    CityViewSet,
    VehicleColorViewSet,
    VehicleBrandViewSet,
    VehicleTypeViewSet,
    VehicleModelViewSet,
    VehicleViewSet,
    TripViewSet,
    Passenger_TripViewSet,
)

'''
if settings.DEBUG :
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()
'''

router = routers.DefaultRouter()

router.register('users', views.CustomUserViewSet, 'CustomUser')
router.register('user-management', ExtendedUserViewSet, 'ExtendedUser')
router.register('userType', UserTypeViewSet, 'UserType')
router.register('city', CityViewSet, 'City')
router.register('vehicleColor', VehicleColorViewSet, 'VehicleColor')
router.register('vehicleBrand', VehicleBrandViewSet, 'VehicleBrand')
router.register('vehicleType', VehicleTypeViewSet, 'VehicleType')
router.register('vehicleModel', VehicleModelViewSet, 'VehicleModel')
router.register('vehicle', VehicleViewSet, 'Vehicle')
router.register('trip', TripViewSet, 'Trip')
router.register('passenger-trip', Passenger_TripViewSet, 'Passenger_Trip')

urlpatterns = [
    path('user-management/list/', views.list_users, name='ListUsers'),
    path('users/registration/', views.registration, name='Registration'),
    path('users/profile/', views.get_profile, name='Profile'),
    path('vehicle/registration/', views.vehicle_registration, name='VehiclesRegistration'),
    path('driver/trip/add/', views.add_trip, name='AddTrip'),
    path('driver/trip/update/<int:id_trip>/', views.update_trip, name='UpdateTrip'),
    path('driver/trip/<int:id_trip>/', views.get_trip, name='GetTrip'),
    path('driver/vehicle/', views.my_vehicles, name='MyVehicles'),
    path('driver/vehicle/add/', views.add_vehicle, name='AddVehicle'),
    path('driver/vehicle/delete/<int:id_vehicle>/', views.delete_vehicle, name='DeleteVehicle'),
    path('driver/vehicle/update/<int:id_vehicle>/', views.update_vehicle, name='UpdateVehicle'),
    path('driver/vehicle/<int:id_vehicle>/', views.get_vehicle, name='GetVehicle'),
    path('driver/home/', views.home_driver, name='HomeDriver'),
    path('passenger/home/', views.home_passenger, name='HomePassenger'),
    path('', include(router.urls)),
]
