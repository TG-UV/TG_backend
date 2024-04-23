from rest_framework import serializers
from api.custom_validators import validate_vehicle_owner
from api.models import Trip
from .user import ViewUserReduceSerializer
from typing import Dict, Any


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


class ViewTripSerializer(ViewTripReduceSerializer):
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


class ViewTripMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'driver',
            'vehicle',
        )
        read_only_fields = fields

    driver = ViewUserReduceSerializer()


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
