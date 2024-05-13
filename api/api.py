from rest_framework import viewsets, permissions
from .serializers.user_type import UserTypeSerializer
from .serializers.city import CitySerializer
from .serializers.user import ExtendedUserSerializer
from .serializers.vehicle_color import VehicleColorSerializer
from .serializers.vehicle_brand import VehicleBrandSerializer
from .serializers.vehicle_type import VehicleTypeSerializer
from .serializers.vehicle_model import VehicleModelSerializer
from .serializers.vehicle import VehicleSerializer
from .serializers.trip import TripSerializer
from .serializers.passenger_trip import Passenger_TripSerializer
from .serializers.device import DeviceSerializer
from .models import (
    UserType,
    City,
    User,
    VehicleColor,
    VehicleBrand,
    VehicleType,
    VehicleModel,
    Vehicle,
    Trip,
    Passenger_Trip,
    Device,
)


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserTypeSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CitySerializer


class ExtendedUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ExtendedUserSerializer


class VehicleColorViewSet(viewsets.ModelViewSet):
    queryset = VehicleColor.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VehicleColorSerializer


class VehicleBrandViewSet(viewsets.ModelViewSet):
    queryset = VehicleBrand.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VehicleBrandSerializer


class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VehicleTypeSerializer


class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = VehicleModel.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VehicleModelSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VehicleSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TripSerializer


class Passenger_TripViewSet(viewsets.ModelViewSet):
    queryset = Passenger_Trip.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = Passenger_TripSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DeviceSerializer
