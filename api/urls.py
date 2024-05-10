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

auth_urls = [ 
    path('token/login/', general.CustomLogin.as_view(), name='custom_login'),
    path('token/logout/', general.CustomLogout.as_view(), name='custom_logout')
]

driver_urls = [
    path('trip/history/', driver.get_trip_history, name='trip_history_driver'),
    path('trip/planned/', driver.get_planned_trips, name='planned_trips_driver'),
    path('trip/current/', driver.get_current_trip, name='current_trip'),
    path('trip/add/', driver.add_trip, name='add_trip'),
    path('trip/delete/<int:id_trip>/', driver.delete_trip, name='delete_trip'),
    path('trip/<int:id_trip>/', driver.get_trip, name='get_trip_driver'),
    path('passenger-trip/confirm/<int:id_passenger_trip>/', driver.confirm_passenger_trip, name='confirm_passenger_trip'),
    path('passenger-trip/delete/<int:id_passenger_trip>/', driver.delete_passenger_trip, name='delete_passenger_trip'),
    path('vehicle/', driver.get_my_vehicles, name='my_vehicles'),
    path('vehicle/add/', driver.add_vehicle, name='add_vehicle'),
    path('vehicle/delete/<int:id_vehicle>/', driver.delete_vehicle, name='delete_vehicle'),
    path('vehicle/update/<int:id_vehicle>/', driver.update_vehicle, name='update_vehicle'),
    path('vehicle/<int:id_vehicle>/', driver.get_vehicle, name='get_vehicle'),
    path('home/', general.home, name='home_driver'),
]

passenger_urls = [
    path('trip/history/', passenger.trip_history, name='trip_history_passenger'),
    path('trip/planned/', passenger.planned_trips, name='planned_trips_passenger'),
    path('trip/book/', passenger.book_trip, name='book_trip'),
    path('trip/delete/<int:id_trip>/', passenger.delete_trip_reservation, name='delete_trip_reservation'),
    path('trip/associated/<int:id_trip>/', passenger.get_trip_associated, name='get_associated_trip_passenger'),
    path('trip/<int:id_trip>/', passenger.get_trip, name='get_trip_passenger'),
    path('search/', passenger.search_route, name='search_route_passenger'),
    path('home/', general.home, name='home_passenger'),
]

users_urls = [
    path('registration/', registration.registration, name='registration'),
    path('profile/', general.get_profile, name='profile'),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('driver/', include(driver_urls)),
    path('passenger/', include(passenger_urls)),
    path('user-management/list/', admin.list_users, name='list_users'),
    path('users/', include(users_urls)),
    path('vehicle/registration/', registration.vehicle_registration, name='vehicles_registration'),
    path('', include(router.urls)),
]
