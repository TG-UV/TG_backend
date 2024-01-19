from rest_framework import serializers
from django.contrib.auth import get_user_model
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


# Convierte los modelo a JSON para las peticiones
'''class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        read_only_fields = ('id_user', 'registration_date')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField()
	password = serializers.CharField()
	token = serializers.CharField(read_only=True)
'''

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


class Driver_VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver_Vehicle
        fields = '__all__'
        read_only_fields = ('id_driver_Vehicle',)


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
