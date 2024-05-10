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

    def annotate_start_datetime(self):
        return self.base_query().annotate(
            start_datetime=ExpressionWrapper(
                F('start_date') + F('start_time'), output_field=DateTimeField()
            )
        )

    def get_trip_history_for(self, current_datetime, driver):
        return (
            self.annotate_start_datetime()
            .filter(start_datetime__lt=current_datetime, driver=driver)
            .order_by('-start_datetime')
        )  # lt significa less than.

    def get_planned_trips_for(self, current_datetime, driver):
        return (
            self.annotate_start_datetime()
            .filter(start_datetime__gt=current_datetime, driver=driver)
            .order_by('start_datetime')
        )  # gt significa greater than.

    def get_current_trip_for(self, current_datetime, two_hours_ago_datetime, driver):
        return (
            self.annotate_start_datetime()
            .filter(
                start_datetime__lte=current_datetime,
                start_datetime__gt=two_hours_ago_datetime,
                driver=driver,
            )
            .order_by('-start_datetime')
            .first()
        )  # lte significa less than equal.

    def get_trip_for_delete(self, id_trip, driver):
        return self.only('id_trip').get(id_trip=id_trip, driver=driver)
