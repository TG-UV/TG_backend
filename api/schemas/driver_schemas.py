from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, inline_serializer
from api.serializers import VehicleSerializer


add_vehicle_schema = {
    'description': 'Vista para registrar un vehículo (requiere token).',
    'request': {
        'application/json': VehicleSerializer,
    },
    'responses': {
        200: VehicleSerializer,
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
            value={
                "count": 10,
                "next": "http://127.0.0.1:8000/driver/vehicle/?page=3",
                "previous": "http://127.0.0.1:8000/driver/vehicle/?page=1",
                "results": [
                    {
                        "id_vehicle": 1,
                        "vehicle_type": "Carro",
                        "vehicle_brand": "Mercedes",
                        "vehicle_model": "2020",
                        "vehicle_color": "Negro",
                        "license_plate": "BC123",
                    },
                    {
                        "id_vehicle": 2,
                        "vehicle_type": "Carro",
                        "vehicle_brand": "Mazda",
                        "vehicle_model": "2024",
                        "vehicle_color": "Gris",
                        "license_plate": "ABC123",
                    },
                ],
            },
            description='En este ejemplo el usuario ha registrado 10 vehículos, así que se '
            + 'muestran algunos vehículos y se proporcionan los enlaces para obtener los '
            + 'siguientes vehículos.',
        ),
        OpenApiExample(
            "Vehicles 2",
            value={
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id_vehicle": 1,
                        "vehicle_type": "Carro",
                        "vehicle_brand": "Mercedes",
                        "vehicle_model": "2020",
                        "vehicle_color": "Negro",
                        "license_plate": "BC123",
                    },
                ],
            },
            description='En este ejemplo el usuario solo ha registrado 1 vehículo por lo que '
            + 'no existen enlaces para mostrar más vehículos.',
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
