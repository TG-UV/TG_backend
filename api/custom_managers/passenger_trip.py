from django.db.models import F, DateTimeField, ExpressionWrapper
from django.db import models


class Passenger_TripManager(models.Manager):
    def base_query(self):
        queryset = self.get_queryset()
        return queryset.only(
            'pickup_point_lat',
            'pickup_point_long',
            'seats',
            'is_confirmed',
        )

    def reservation_with_passenger_query(self):
        queryset = self.get_queryset()
        return queryset.select_related('passenger').only(
            'passenger',
            'pickup_point_lat',
            'pickup_point_long',
            'seats',
            'is_confirmed',
            'passenger__phone_number',
            'passenger__first_name',
            'passenger__last_name',
        )

    def trip_info_query(self):
        queryset = self.get_queryset()
        return queryset.select_related('trip').only(
            'trip',
            'trip__start_date',
            'trip__start_time',
            'trip__starting_point_lat',
            'trip__starting_point_long',
            'trip__arrival_point_lat',
            'trip__arrival_point_long',
        )

    def annotate_start_datetime(self):
        return self.trip_info_query().annotate(
            start_datetime=ExpressionWrapper(
                F('trip__start_date') + F('trip__start_time'),
                output_field=DateTimeField(),
            )
        )

    def get_passengers(self, id_trip):
        return self.reservation_with_passenger_query().filter(trip=id_trip)

    def get_basic_reservation_info(self, id_passenger_trip, driver):
        return (
            self.select_related('trip')
            .only('seats', 'is_confirmed', 'trip__seats')
            .get(id_passenger_trip=id_passenger_trip, trip__driver=driver)
        )

    def get_reservation(self, id_trip, passenger):
        return self.base_query().get(trip=id_trip, passenger=passenger)

    def get_data_to_delete_reservation(self, id_passenger_trip, driver):
        return self.only('seats', 'is_confirmed', 'trip_id').get(
            id_passenger_trip=id_passenger_trip, trip__driver=driver
        )

    def get_trip_history(self, start_datetime, passenger):
        return (
            self.annotate_start_datetime()
            .filter(start_datetime__lt=start_datetime, passenger=passenger)
            .order_by('-start_datetime')
        )  # lt significa less than.

    def get_planned_trips(self, start_datetime, passenger):
        return (
            self.annotate_start_datetime()
            .filter(start_datetime__gt=start_datetime, passenger=passenger)
            .order_by('start_datetime')
        )  # gt significa greater than.
