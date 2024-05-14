from django.db.models import F, DateTimeField, ExpressionWrapper
from django.db import models


class TripManager(models.Manager):
    def base_query(self):
        queryset = self.get_queryset()
        return queryset.only(
            'id_trip',
            'start_date',
            'start_time',
            'starting_point_lat',
            'starting_point_long',
            'arrival_point_lat',
            'arrival_point_long',
            'seats',
            'fare',
        )

    def trip_with_driver_and_vehicle_query(self):
        queryset = self.get_queryset()
        return queryset.select_related(
            'driver',
            'vehicle',
            'vehicle__vehicle_type',
            'vehicle__vehicle_brand',
            'vehicle__vehicle_model',
            'vehicle__vehicle_color',
        ).only(
            'start_date',
            'start_time',
            'starting_point_lat',
            'starting_point_long',
            'arrival_point_lat',
            'arrival_point_long',
            'seats',
            'fare',
            'current_trip',
            'driver__first_name',
            'driver__last_name',
            'driver__phone_number',
            'vehicle',
        )

    def driver_and_vehicle_from_trip_query(self):
        queryset = self.get_queryset()
        return queryset.select_related(
            'driver',
            'vehicle',
            'vehicle__vehicle_type',
            'vehicle__vehicle_brand',
            'vehicle__vehicle_model',
            'vehicle__vehicle_color',
        ).only(
            'vehicle',
            'driver__first_name',
            'driver__last_name',
            'driver__phone_number',
        )

    def annotate_start_datetime(self):
        return self.base_query().annotate(
            start_datetime=ExpressionWrapper(
                F('start_date') + F('start_time'), output_field=DateTimeField()
            )
        )

    def get_trip_history(self, start_datetime, driver):
        return (
            self.annotate_start_datetime()
            .filter(start_datetime__lt=start_datetime, driver=driver)
            .order_by('-start_datetime')
        )  # lt significa less than.

    def get_planned_trips(self, start_datetime, driver):
        return (
            self.annotate_start_datetime()
            .filter(start_datetime__gt=start_datetime, driver=driver)
            .order_by('start_datetime')
        )  # gt significa greater than.

    def get_current_trip(self, max_start_datetime, min_start_datetime, driver):
        return (
            self.annotate_start_datetime()
            .filter(
                start_datetime__lte=max_start_datetime,
                start_datetime__gt=min_start_datetime,
                driver=driver,
            )
            .order_by('-start_datetime')
            .first()
        )  # lte significa less than equal.

    def search_trips(self, start_date, start_time, seats):
        return (
            self.base_query()
            .filter(start_date=start_date, start_time__gte=start_time, seats__gte=seats)
            .order_by('start_time')
        )  # gte significa greater than equal.

    def get_trip_with_driver_and_vehicle(self, id_trip):
        return self.trip_with_driver_and_vehicle_query().get(id_trip=id_trip)

    def get_driver_and_vehicle_from_trip(self, id_trip):
        return self.driver_and_vehicle_from_trip_query().get(id_trip=id_trip)
