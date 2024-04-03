from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, inline_serializer
from api.serializers import VehicleSerializer, TripSerializer


add_vehicle_schema = {
    'description': 'Vista para registrar un vehículo (requiere token).',
    'request': {
        'application/json': VehicleSerializer,
    },
    'responses': {
        201: VehicleSerializer,
    },
    'examples': [
        OpenApiExample(
            "Add vehicle request",
            value={
                "license_plate": "ABC123",
                "vehicle_type": 1,
                "vehicle_brand": 1,
                "vehicle_model": 1,
                "vehicle_color": 1,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Add vehicle response",
            value={
                "id_vehicle": 2,
                "license_plate": "ABC123",
                "vehicle_type": 1,
                "vehicle_brand": 1,
                "vehicle_model": 1,
                "vehicle_color": 1,
                "owner": 3,
            },
            description='En este ejemplo el vehículo fue creado por el usuario de id 3.',
            response_only=True,
        ),
    ],
}

view_vehicle_serializer = inline_serializer(
    name="ViewVehicle",
    fields={
        "id_vehicle": serializers.IntegerField(),
        "vehicle_type": serializers.CharField(),
        "vehicle_brand": serializers.CharField(),
        "vehicle_model": serializers.CharField(),
        "vehicle_color": serializers.CharField(),
        "license_plate": serializers.CharField(),
    },
)

get_vehicle_schema = {
    'description': 'Datos de un vehículo registrado por un usuario (requiere token).',
    'responses': {
        200: view_vehicle_serializer,
    },
    'examples': [
        OpenApiExample(
            "Vehicle",
            value={
                "id_vehicle": 14,
                "vehicle_type": "Carro",
                "vehicle_brand": "Mercedes",
                "vehicle_model": "2024",
                "vehicle_color": "Negro",
                "license_plate": "ABC321",
            },
            description='En este ejemplo el id de la url es 14: .../driver/vehicle/14/.',
        ),
    ],
}

my_vehicles_schema = {
    'description': 'Vehículos registrados por un usuario (requiere token).',
    'responses': {
        200: view_vehicle_serializer,
    },
    'examples': [
        OpenApiExample(
            "Vehicles",
            value=[
                {
                    "id_vehicle": 1,
                    "vehicle_type": "Carro",
                    "vehicle_brand": "Mercedes",
                    "vehicle_model": "2020",
                    "vehicle_color": "Negro",
                    "license_plate": "ABC123",
                },
                {
                    "id_vehicle": 2,
                    "vehicle_type": "Carro",
                    "vehicle_brand": "Mazda",
                    "vehicle_model": "2024",
                    "vehicle_color": "Gris",
                    "license_plate": "BC123",
                },
            ],
            description='En este ejemplo el usuario ha registrado 2 vehículos. Se cambian'
            + ' los ids por los nombres de los campos.',
        ),
        OpenApiExample(
            "Vehicles 2",
            value=[
                {
                    "id_vehicle": 1,
                    "vehicle_type": "Carro",
                    "vehicle_brand": "Mercedes",
                    "vehicle_model": "2020",
                    "vehicle_color": "Negro",
                    "license_plate": "BC123",
                },
            ],
            description='En este ejemplo el usuario solo ha registrado 1 vehículo.',
        ),
    ],
}

delete_vehicle_schema = {
    'description': 'Vista para eliminar un vehículo registrado por un usuario (requiere token).',
    'responses': {
        204: inline_serializer(
            name="VehicleDeleted",
            fields={},
        ),
    },
}

update_vehicle_schema = {
    'description': 'Vista para actualizar los datos de un vehículo (requiere token).',
    'request': {
        'application/json': VehicleSerializer,
    },
    'responses': {
        200: VehicleSerializer,
    },
    'examples': [
        OpenApiExample(
            "Update vehicle PUT request",
            value={
                "license_plate": "ABC123",
                "vehicle_type": 1,
                "vehicle_brand": 1,
                "vehicle_model": 1,
                "vehicle_color": 1,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Update vehicle PATCH request",
            value={
                "license_plate": "ABC123",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Update vehicle response",
            value={
                "id_vehicle": 2,
                "license_plate": "ABC123",
                "vehicle_type": 1,
                "vehicle_brand": 1,
                "vehicle_model": 1,
                "vehicle_color": 1,
                "owner": 3,
            },
            description='En este ejemplo el vehículo con id 2 fue actualizado, la url sería: '
            + '.../driver/vehicle/update/2/.',
            response_only=True,
        ),
    ],
}

add_trip_schema = {
    'description': 'Vista para registrar un viaje (requiere token).',
    'request': {
        'application/json': TripSerializer,
    },
    'responses': {
        201: TripSerializer,
    },
    'examples': [
        OpenApiExample(
            "Add trip request",
            value={
                "start_date": "2024-04-01",
                "start_time": "18:00:00",
                "starting_point": "Norte",
                "arrival_point": "Univalle",
                "seats": 4,
                "fare": 5000,
                "current_trip": False,
                "vehicle": 2,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Add trip response",
            value={
                "id_trip": 1,
                "start_date": "2024-04-01",
                "start_time": "18:00:00",
                "starting_point": "Norte",
                "arrival_point": "Univalle",
                "seats": 4,
                "fare": 5000,
                "current_trip": False,
                "driver": 3,
                "vehicle": 2,
            },
            description='En este ejemplo el viaje fue creado por el usuario de id 3.'
            + ' El vehículo 2 le pertenece a ese usuario.',
            response_only=True,
        ),
    ],
}


update_trip_schema = {
    'description': 'Vista para actualizar los datos de un viaje (requiere token).',
    'request': {
        'application/json': TripSerializer,
    },
    'responses': {
        200: TripSerializer,
    },
    'examples': [
        OpenApiExample(
            "Update trip PUT request",
            value={
                "start_date": "2024-04-02",
                "start_time": "07:00:00",
                "starting_point": "Palmira",
                "arrival_point": "Univalle",
                "seats": 4,
                "fare": 10000,
                "current_trip": False,
                "driver": 3,
                "vehicle": 21,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Update trip PATCH request",
            value={
                "seats": 2,
                "current_trip": True,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Update trip response",
            value={
                "id_trip": "1",
                "start_date": "2024-04-02",
                "start_time": "07:00:00",
                "starting_point": "Palmira",
                "arrival_point": "Univalle",
                "seats": 4,
                "fare": 10000,
                "current_trip": False,
                "driver": 3,
                "vehicle": 21,
            },
            description='En este ejemplo el viaje con id 1 fue actualizado, la url sería: '
            + '.../driver/trip/update/1/.',
            response_only=True,
        ),
    ],
}


view_trip_serializer = inline_serializer(
    name="ViewTrip",
    fields={
        "id_trip": serializers.IntegerField(),
        "start_date": serializers.DateField(),
        "start_time": serializers.TimeField(),
        "starting_point": serializers.CharField(),
        "arrival_point": serializers.CharField(),
        "seats": serializers.IntegerField(),
        "fare": serializers.IntegerField(),
        "current_trip": serializers.BooleanField(),
        "driver": serializers.IntegerField(),
        "vehicle": serializers.DictField(),
        "confirmed_passengers": serializers.ListField(),
        "pending_passengers": serializers.ListField(),
    },
)

get_trip_schema = {
    'description': 'Datos de un viaje registrado por un usuario (requiere token).',
    'responses': {
        200: view_trip_serializer,
    },
    'examples': [
        OpenApiExample(
            "Trip",
            value={
                "id_trip": 1,
                "vehicle": {
                    "id_vehicle": 21,
                    "license_plate": "OKK123",
                    "vehicle_type": "Carro",
                    "vehicle_brand": "Mercedes",
                    "vehicle_model": "2024",
                    "vehicle_color": "Negro",
                },
                "start_date": "2024-04-02",
                "start_time": "02:56:51",
                "starting_point": "Terminal",
                "arrival_point": "Univalle",
                "seats": 4,
                "fare": 10000,
                "current_trip": False,
                "driver": 3,
                "confirmed_passengers": [
                    {
                        "id_passenger_trip": 2,
                        "passenger": {
                            "id_passenger": 35,
                            "phone_number": "3206678",
                            "first_name": "Carlos",
                            "last_name": "García",
                        },
                        "pickup_point": "Casa",
                        "seats": 1,
                        "is_confirmed": True,
                        "trip": 1,
                    }
                ],
                "pending_passengers": [
                    {
                        "id_passenger_trip": 1,
                        "passenger": {
                            "id_passenger": 10,
                            "phone_number": "3204654442",
                            "first_name": "Aura",
                            "last_name": "Aaa",
                        },
                        "pickup_point": "Casa",
                        "seats": 2,
                        "is_confirmed": False,
                        "trip": 1,
                    }
                ],
            },
            description='En este ejemplo el id de la url es 1: .../driver/trip/1/.',
        ),
    ],
}
