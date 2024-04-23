from rest_framework import serializers
from api.custom_validators import (
    validate_driver,
)
from api.models import Vehicle


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


class VehicleSerializerNoValidation(serializers.ModelSerializer):
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
        return obj.vehicle_type.name

    def get_vehicle_brand(self, obj):
        return obj.vehicle_brand.name

    def get_vehicle_model(self, obj):
        return obj.vehicle_model.name

    def get_vehicle_color(self, obj):
        return obj.vehicle_color.name


class ViewVehicleReduceSerializer(ViewVehicleSerializer):
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
