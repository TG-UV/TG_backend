from django.db import models


class Passenger_TripManager(models.Manager):
    def base_query(self):
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

    def get_passengers(self, id_trip):
        return self.base_query().filter(trip=id_trip)

    def get_basic_reservation_info(self, id_passenger_trip, id_user):
        return (
            self.select_related('trip')
            .only('seats', 'is_confirmed', 'trip__seats')
            .get(id_passenger_trip=id_passenger_trip, trip__driver=id_user)
        )

    def get_data_to_delete_reservation(self, id_passenger_trip, id_user):
        return self.only('seats', 'is_confirmed', 'trip_id').get(
            id_passenger_trip=id_passenger_trip, trip__driver=id_user
        )
