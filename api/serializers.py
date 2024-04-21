from rest_framework import serializers
from djoser.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UsernameSerializer,
    CurrentPasswordSerializer,
)
from api import error_messages
from .custom_validators import (
    validate_driver,
    validate_passenger,
    validate_vehicle_owner,
    validate_email_domain,
    ALLOWED_EMAIL_DOMAIN,
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
from typing import Dict, Any


# Convierte los modelo a JSON para las peticiones.
class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'
        read_only_fields = ('id_user_type',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        read_only_fields = ('id_city',)


class ExtendedUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id_user',
            'email',
            'identity_document',
            'phone_number',
            'first_name',
            'last_name',
            'date_of_birth',
            'password',
            'registration_date',
            'residence_city',
            'type',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
        )
        read_only_fields = (
            'id_user',
            'registration_date',
            'last_login',
            'is_staff',
            'is_superuser',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }  # Para que no se pueda ver.

    def create(self, validated_data):
        user_type = validated_data['type']

        if user_type.name == 'Admin':
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        user_type = validated_data.get('type', instance.type)
        password = validated_data.pop('password', None)

        if user_type.name == 'Admin':
            validated_data['is_staff'] = True
            validated_data['is_superuser'] = True
        else:
            validated_data['is_staff'] = False
            validated_data['is_superuser'] = False

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CustomUserCreateSerializer(UserCreateSerializer):

    def validate(self, attrs):
        email = attrs['email']
        user_type = attrs['type']
        allowed_types = ['Conductor', 'Pasajero']
        errors = {}

        # Validaciones de Django.
        attrs = super().validate(attrs)

        # Valida que solo se puedan registrar Conductores o Pasajeros.
        if user_type.name not in allowed_types:
            errors['type'] = error_messages.INVALID_USER_TYPE

        # Valida el dominio del correo.
        if not email.endswith(ALLOWED_EMAIL_DOMAIN):
            errors['email'] = error_messages.EMAIL_DOMAIN_NOT_ALLOWED

        if not errors:
            return attrs
        else:
            raise serializers.ValidationError(errors)


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'id_user',
            'email',
            'identity_document',
            'phone_number',
            'first_name',
            'last_name',
            'date_of_birth',
            'residence_city',
            'type',
            'is_active',
        )
        read_only_fields = ('id_user', 'email', 'type')


class ViewUserSerializer(CustomUserSerializer):
    residence_city = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_residence_city(self, obj):
        return obj.residence_city.name if obj.residence_city else None

    def get_type(self, obj):
        return obj.type.name if obj.type else None


class ViewUserReduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'phone_number',
            'first_name',
            'last_name',
        )
        read_only_fields = fields


class CustomSetUsernameSerializer(UsernameSerializer, CurrentPasswordSerializer):
    class Meta:
        model = User
        fields = ('email', 'current_password')

    def validate(self, attrs):
        email = attrs['email']

        # Validaciones de Django.
        attrs = super().validate(attrs)

        # Valida el dominio del correo.
        validate_email_domain(email)

        return attrs


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

    def validate(self, attrs):
        owner = attrs.get('owner', None)

        if owner:
            validate_driver(owner)

        return attrs


class VehicleSerializerForDriver(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ('id_vehicle',)


class ViewVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            'id_vehicle',
            'vehicle_type',
            'vehicle_brand',
            'vehicle_model',
            'vehicle_color',
            'license_plate',
        )
        read_only_fields = fields

    vehicle_type = serializers.SerializerMethodField()
    vehicle_brand = serializers.SerializerMethodField()
    vehicle_model = serializers.SerializerMethodField()
    vehicle_color = serializers.SerializerMethodField()

    def get_vehicle_type(self, obj):
        return obj.vehicle_type.name if obj.vehicle_type else None

    def get_vehicle_brand(self, obj):
        return obj.vehicle_brand.name if obj.vehicle_brand else None

    def get_vehicle_model(self, obj):
        return obj.vehicle_model.name if obj.vehicle_model else None

    def get_vehicle_color(self, obj):
        return obj.vehicle_color.name if obj.vehicle_color else None


class ViewVehicleSerializerForPassenger(ViewVehicleSerializer):
    class Meta:
        model = Vehicle
        fields = (
            'vehicle_type',
            'vehicle_brand',
            'vehicle_model',
            'vehicle_color',
            'license_plate',
        )
        read_only_fields = fields


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('id_trip',)

    def validate(self, attrs):
        driver = attrs.get('driver', None)
        vehicle = attrs.get('vehicle', None)

        if driver and vehicle:
            validate_vehicle_owner(driver, vehicle)

        return attrs


class ViewTripReduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'id_trip',
            'start_date',
            'start_time',
            'starting_point',
            'arrival_point',
        )
        read_only_fields = fields

    starting_point = serializers.SerializerMethodField()
    arrival_point = serializers.SerializerMethodField()

    def get_starting_point(self, obj):
        return {
            'lat': obj.starting_point_lat,
            'long': obj.starting_point_long,
        }

    def get_arrival_point(self, obj):
        return {
            'lat': obj.arrival_point_lat,
            'long': obj.arrival_point_long,
        }


class ViewTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'id_trip',
            'driver',
            'start_date',
            'start_time',
            'starting_point',
            'arrival_point',
            'seats',
            'fare',
            'current_trip',
            'vehicle',
        )
        read_only_fields = fields

    driver = ViewUserReduceSerializer()
    starting_point = serializers.SerializerMethodField()
    arrival_point = serializers.SerializerMethodField()

    def get_starting_point(self, obj):
        return {
            'lat': obj.starting_point_lat,
            'long': obj.starting_point_long,
        }

    def get_arrival_point(self, obj):
        return {
            'lat': obj.arrival_point_lat,
            'long': obj.arrival_point_long,
        }


class ViewTripDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'driver',
            'vehicle',
        )
        read_only_fields = fields

    driver = ViewUserReduceSerializer()


class Passenger_TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger_Trip
        fields = '__all__'
        read_only_fields = ('id_passenger_trip',)

    def validate(self, attrs):
        passenger = attrs.get('passenger', None)

        if passenger:
            validate_passenger(passenger)

        return attrs


class ViewPassenger_TripSerializerForDriver(serializers.ModelSerializer):

    class Meta:
        model = Passenger_Trip
        fields = (
            'id_passenger_trip',
            'passenger',
            'pickup_point',
            'seats',
            'is_confirmed',
        )
        read_only_fields = fields

    passenger = ViewUserReduceSerializer()
    pickup_point = serializers.SerializerMethodField()

    def get_pickup_point(self, obj):
        return {
            'lat': obj.pickup_point_lat,
            'long': obj.pickup_point_long,
        }


class ViewPassenger_TripSerializerForPassenger(serializers.ModelSerializer):

    class Meta:
        model = Passenger_Trip
        fields = (
            'id_passenger_trip',
            'pickup_point',
            'seats',
            'is_confirmed',
        )
        read_only_fields = fields

    pickup_point = serializers.SerializerMethodField()

    def get_pickup_point(self, obj):
        return {
            'lat': obj.pickup_point_lat,
            'long': obj.pickup_point_long,
        }


def serialize_passenger_trip(passenger_Trip: Passenger_Trip) -> Dict[str, Any]:
    return {
        'id_trip': passenger_Trip.trip.id_trip,
        'start_date': passenger_Trip.trip.start_date,
        'start_time': passenger_Trip.trip.start_time,
        'starting_point': {
            'lat': passenger_Trip.trip.starting_point_lat,
            'long': passenger_Trip.trip.starting_point_long,
        },
        'arrival_point': {
            'lat': passenger_Trip.trip.arrival_point_lat,
            'long': passenger_Trip.trip.arrival_point_long,
        },
    }


def planned_trips_driver_serializer(trip: Trip) -> Dict[str, Any]:
    return {
        'id_trip': trip.id_trip,
        'start_date': trip.start_date,
        'start_time': trip.start_time,
        'starting_point': {
            'lat': trip.starting_point_lat,
            'long': trip.starting_point_long,
        },
        'arrival_point': {
            'lat': trip.arrival_point_lat,
            'long': trip.arrival_point_long,
        },
        'seats': trip.seats,
        'fare': trip.fare,
    }
