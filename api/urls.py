from rest_framework import routers
from .api import (
    DriverViewSet,
    PassengerViewSet,
    VehicleColorViewSet,
    VehicleBrandViewSet,
    VehicleTypeViewSet,
    VehicleModelViewSet,
    VehicleViewSet,
    AdminViewSet,
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
router.register('api/Admin', AdminViewSet, 'Admin')
router.register('api/Trip', TripViewSet, 'Trip')
router.register('api/PassangerTrip', PassangerTripViewSet, 'PassangerTrip')

urlpatterns = router.urls
