from rest_framework import routers
from django.urls import path, include
from api import views
from .api import (
    UserTypeViewSet,
    CityViewSet,
    UserCustomViewSet,
    VehicleColorViewSet,
    VehicleBrandViewSet,
    VehicleTypeViewSet,
    VehicleModelViewSet,
    VehicleViewSet,
    TripViewSet,
    Passenger_TripViewSet,
)

router = routers.DefaultRouter()

router.register('user', UserCustomViewSet, 'UserCustom')
router.register('userType', UserTypeViewSet, 'UserType')
router.register('city', CityViewSet, 'Passenger')
router.register('vehicleColor', VehicleColorViewSet, 'VehicleColor')
router.register('vehicleBrand', VehicleBrandViewSet, 'VehicleBrand')
router.register('vehicleType', VehicleTypeViewSet, 'VehicleType')
router.register('vehicleModel', VehicleModelViewSet, 'VehicleModel')
router.register('vehicle', VehicleViewSet, 'Vehicle')
router.register('trip', TripViewSet, 'Trip')
router.register('passenger-trip', Passenger_TripViewSet, 'Passenger_Trip')

urlpatterns = [
    path('user/list/', views.list_users, name='ListUsers'),
    # path(
    #    'create_superuser/', views.CreateSuperuserView.as_view(), name='CreateSuperuser'
    # ),
    # path('update_user/', views.UpdateSuperuserView.as_view(), name='UpdateSuperuser'),
    path('user/registration/', views.registration, name='Registration'),
    path('vehicle/registration/', views.vehicle_registration, name='VehiclesRegistration'),
    path('driver/vehicle/', views.my_vehicles, name='MyVehicles'),
    path('driver/vehicle/add/', views.add_vehicle, name='AddVehicle'),
    path('driver/vehicle/<int:id>/', views.get_vehicle, name='GetVehicle'),
    path('driver/home/', views.home_driver, name='HomeDriver'),
    path('passenger/home/', views.home_passenger, name='HomePassenger'),
    path('', include(router.urls)),
]
