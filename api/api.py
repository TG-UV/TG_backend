from rest_framework import viewsets, permissions
from .serializers import (
    DriverSerializer,
    PassengerSerializer,
    VehicleColorSerializer,
    VehicleBrandSerializer,
    VehicleTypeSerializer,
    VehicleModelSerializer,
    VehicleSerializer,
    Driver_VehicleSerializer,
    TripSerializer,
    PassangerTripSerializer,
)
from .models import (
    Driver,
    Passenger,
    VehicleColor,
    VehicleBrand,
    VehicleType,
    VehicleModel,
    Vehicle,
    Driver_Vehicle,
    Trip,
    PassangerTrip,
)


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


class PassangerTripViewSet(viewsets.ModelViewSet):
    queryset = PassangerTrip.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PassangerTripSerializer
