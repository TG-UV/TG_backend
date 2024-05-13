from rest_framework import serializers
from api.custom_validators import validate_passenger
from api.models import Passenger_Trip
from .user import ViewUserReduceSerializer


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


class ViewPassenger_TripReduceSerializer(serializers.ModelSerializer):
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


class ViewPassenger_TripSerializer(ViewPassenger_TripReduceSerializer):
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
