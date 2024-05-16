from rest_framework import serializers
from api.custom_validators import validate_vehicle_owner, validate_start_datetime
from api.models import Trip
from .vehicle import ViewVehicleReduceSerializer
from .user import ViewUserReduceSerializer
from typing import Dict, Any
from datetime import datetime


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('id_trip',)

    def validate(self, attrs):
        driver = attrs.get('driver', None)
        vehicle = attrs.get('vehicle', None)
        start_date = attrs.get('start_date', None)
        start_time = attrs.get('start_time', None)

        if driver and vehicle:
            validate_vehicle_owner(driver, vehicle)

        if start_date and start_time:
            start_datetime = datetime.combine(start_date, start_time)
            validate_start_datetime(start_datetime)

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
            'seats',
            'fare',
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
    vehicle = ViewVehicleReduceSerializer()


class ViewTripMinimalSerializer(ViewTripSerializer):
    class Meta:
        model = Trip
        fields = (
            'driver',
            'vehicle',
        )
        read_only_fields = fields


class TripSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'start_date',
            'start_time',
            'starting_point_lat',
            'starting_point_long',
            'arrival_point_lat',
            'arrival_point_long',
            'seats',
        )


def trip_reduce_serializer(trip: Trip) -> Dict[str, Any]:
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
    }


def planned_trips_serializer(trip: Trip) -> Dict[str, Any]:
    return {
        **trip_reduce_serializer(trip),
        'seats': trip.seats,
        'fare': trip.fare,
    }
