from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from .views import (
    admin,
    driver,
    general,
    passenger,
    registration,
)
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

if settings.PRODUCTION:
    router = routers.SimpleRouter()
else:
    router = routers.DefaultRouter()

router.register('users', general.CustomUserViewSet, 'custom_user')
router.register('user-management', ExtendedUserViewSet, 'extended_user')
router.register('userType', UserTypeViewSet, 'user_type')
router.register('city', CityViewSet, 'city')
router.register('vehicleColor', VehicleColorViewSet, 'vehicle_color')
router.register('vehicleBrand', VehicleBrandViewSet, 'vehicle_brand')
router.register('vehicleType', VehicleTypeViewSet, 'vehicle_type')
router.register('vehicleModel', VehicleModelViewSet, 'vehicle_model')
router.register('vehicle', VehicleViewSet, 'vehicle')
router.register('trip', TripViewSet, 'trip')
router.register('passenger-trip', Passenger_TripViewSet, 'passenger-trip')

urlpatterns = [
    path('user-management/list/', admin.list_users, name='list_users'),
    path('users/registration/', registration.registration, name='registration'),
    path('users/profile/', general.get_profile, name='profile'),
    path('vehicle/registration/', registration.vehicle_registration, name='vehicles_registration'),
    path('driver/trip/history/', driver.trip_history, name='trip_history_driver'),
    path('driver/trip/planned/', driver.planned_trips, name='planned_trips_driver'),
    path('driver/trip/current/', driver.current_trip, name='current_trip'),
    path('driver/trip/add/', driver.add_trip, name='add_trip'),
    path('driver/trip/delete/<int:id_trip>/', driver.delete_trip, name='delete_trip'),
    path('driver/trip/<int:id_trip>/', driver.get_trip, name='get_trip_driver'),
    path('driver/vehicle/', driver.my_vehicles, name='my_vehicles'),
    path('driver/vehicle/add/', driver.add_vehicle, name='add_vehicle'),
    path('driver/vehicle/delete/<int:id_vehicle>/', driver.delete_vehicle, name='delete_vehicle'),
    path('driver/vehicle/update/<int:id_vehicle>/', driver.update_vehicle, name='update_vehicle'),
    path('driver/vehicle/<int:id_vehicle>/', driver.get_vehicle, name='get_vehicle'),
    path('driver/home/', general.home, name='home_driver'),
    path('passenger/trip/history/', passenger.trip_history, name='trip_history_passenger'),
    path('passenger/trip/planned/', passenger.planned_trips, name='planned_trips_passenger'),
    path('passenger/trip/delete/<int:id_trip>/', passenger.delete_trip_reservation, name='delete_trip_reservation'),
    path('passenger/trip/associated/<int:id_trip>/', passenger.get_trip_associated, name='get_associated_trip_passenger'),
    path('passenger/trip/<int:id_trip>/', passenger.get_trip, name='get_trip_passenger'),
    path('passenger/home/', general.home, name='home_passenger'),
    path('', include(router.urls)),
]
