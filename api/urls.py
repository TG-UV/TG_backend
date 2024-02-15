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
router.register('passenger_trip', Passenger_TripViewSet, 'Passenger_Trip')

urlpatterns = [
    path('user/list/', views.ListUsersView.as_view(), name='ListUsers'),
    # path(
    #    'create_superuser/', views.CreateSuperuserView.as_view(), name='CreateSuperuser'
    # ),
    # path('update_user/', views.UpdateSuperuserView.as_view(), name='UpdateSuperuser'),
    path('driver/home/', views.home_driver, name='HomeDriver'),
    path('passenger/home/', views.home_passenger, name='HomePassenger'),
    path('', include(router.urls)),
]
