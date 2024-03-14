from rest_framework import serializers
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


class UserCustomSerializer(serializers.ModelSerializer):
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
        read_only_fields = ('id_user', 'registration_date', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}  # Para que no se pueda ver.

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


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


class ViewVehicleSerializer(serializers.ModelSerializer):
    vehicle_type = serializers.SerializerMethodField()
    vehicle_brand = serializers.SerializerMethodField()
    vehicle_model = serializers.SerializerMethodField()
    vehicle_color = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = '__all__'

    def get_vehicle_type(self, obj):
        return obj.vehicle_type.name if obj.vehicle_type else None

    def get_vehicle_brand(self, obj):
        return obj.vehicle_brand.name if obj.vehicle_brand else None

    def get_vehicle_model(self, obj):
        return obj.vehicle_model.name if obj.vehicle_model else None

    def get_vehicle_color(self, obj):
        return obj.vehicle_color.name if obj.vehicle_color else None

    def get_owner(self, obj):
        return obj.owner.first_name + ' ' + obj.owner.last_name if obj.owner else None


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('id_trip',)


class Passenger_TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger_Trip
        fields = '__all__'
        read_only_fields = ('id_passenger_trip',)
