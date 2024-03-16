from rest_framework import viewsets, permissions
from .serializers import (
    UserTypeSerializer,
    CitySerializer,
    UserExtendedSerializer,
    VehicleColorSerializer,
    VehicleBrandSerializer,
    VehicleTypeSerializer,
    VehicleModelSerializer,
    VehicleSerializer,
    TripSerializer,
    Passenger_TripSerializer,
)
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
)


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserTypeSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CitySerializer


class UserExtendedViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserExtendedSerializer


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
