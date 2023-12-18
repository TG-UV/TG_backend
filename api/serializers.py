from rest_framework import serializers
from .models import (
    Driver,
    Passenger,
    VehicleColor,
    VehicleBrand,
    VehicleType,
    VehicleModel,
    Vehicle,
    Admin,
    Trip,
    PassangerTrip,
)


# Convierte los modelo a JSON para las peticiones
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ('id', 'registration_date')


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'
        read_only_fields = ('id_passenger', 'registration_date')


class VehicleColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleColor
        fields = '__all__'
        read_only_fields = ('id_vehicle_color',)


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = '__all__'
        read_only_fields = ('id_vehicle_brand',)


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'
        read_only_fields = ('id_vehicle_type',)


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = '__all__'
        read_only_fields = ('id_vehicle_model',)


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ('id_vehicle',)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
        read_only_fields = ('id_admin', 'registration_date')


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('id_trip',)


class PassangerTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassangerTrip
        fields = '__all__'
        read_only_fields = ('id_passanger_trip',)
