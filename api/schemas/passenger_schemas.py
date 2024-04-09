from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, inline_serializer

view_trip_serializer_for_passenger = inline_serializer(
    name="ViewTripForPassenger",
    fields={
        "id_passenger_trip": serializers.IntegerField(),
        "pickup_point": serializers.CharField(),
        "seats": serializers.IntegerField(),
        "is_confirmed": serializers.BooleanField(),
        "trip": serializers.ListField(),
    },
)

get_trip_passenger_associated = {
    'description': 'Detalles de un viaje (requiere token).',
    'responses': {
        200: view_trip_serializer_for_passenger,
    },
    'examples': [
        OpenApiExample(
            "Get trip",
            value={
                "id_passenger_trip": 1,
                "pickup_point": "Casa",
                "seats": 2,
                "is_confirmed": True,
                "trip": {
                    "id_trip": 1,
                    "driver": {
                        "phone_number": "3224224444",
                        "first_name": "Carlos",
                        "last_name": "Dd",
                    },
                    "start_date": "2024-04-02",
                    "start_time": "02:56:51",
                    "starting_point": "Casa",
                    "arrival_point": "Univalle",
                    "seats": 1,
                    "fare": 1990,
                    "current_trip": False,
                    "vehicle": {
                        "id_vehicle": 21,
                        "vehicle_type": "Carro",
                        "vehicle_brand": "Mercedes",
                        "vehicle_model": "2024",
                        "vehicle_color": "Negro",
                        "license_plate": "OKK123",
                    },
                },
            },
            description='En este ejemplo el id de la url es 1: .../passenger/trip/1/.',
        ),
    ],
}
