from rest_framework import viewsets, permissions, generics
from .serializers import (
    UserSerializer,
    DriverSerializer,
    PassengerSerializer,
    VehicleColorSerializer,
    VehicleBrandSerializer,
    VehicleTypeSerializer,
    VehicleModelSerializer,
    VehicleSerializer,
    Driver_VehicleSerializer,
    TripSerializer,
    Passenger_TripSerializer,
)
from .models import (
    User,
    Driver,
    Passenger,
    VehicleColor,
    VehicleBrand,
    VehicleType,
    VehicleModel,
    Vehicle,
    Driver_Vehicle,
    Trip,
    Passenger_Trip,
)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    permission_classes = [permissions.AllowAny]  # Cualquier cliente
    serializer_class = DriverSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PassengerSerializer


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


class Driver_VehicleViewSet(viewsets.ModelViewSet):
    queryset = Driver_Vehicle.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = Driver_VehicleSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TripSerializer


class Passenger_TripViewSet(viewsets.ModelViewSet):
    queryset = Passenger_Trip.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = Passenger_TripSerializer
