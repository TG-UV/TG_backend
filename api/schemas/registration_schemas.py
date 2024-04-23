from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, inline_serializer

registration_schema = {
    'description': 'Datos necesarios para registrar un usuario.',
    'responses': {
        200: inline_serializer(
            name="Registration",
            fields={
                "id_city": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
        ),
    },
    'examples': [
        OpenApiExample(
            "Registration",
            value=[
                {"id_city": 1, "name": "Cali"},
                {"id_city": 2, "name": "Palmira"},
                {"id_city": 3, "name": "Jamundí"},
            ],
        ),
    ],
}

vehicle_registration_schema = {
    'description': 'Datos necesarios para registrar un vehículo.',
    'responses': {
        200: inline_serializer(
            name="VehicleRegistration",
            fields={
                "types": serializers.ListField(),
                "brands": serializers.ListField(),
                "models": serializers.ListField(),
                "colors": serializers.ListField(),
            },
        ),
    },
    'examples': [
        OpenApiExample(
            "Vehicle registration",
            value={
                "types": [
                    {"id_vehicle_type": 1, "name": "Carro"},
                    {"id_vehicle_type": 2, "name": "Moto"},
                ],
                "brands": [
                    {"id_vehicle_brand": 1, "name": "Chevrolet"},
                    {"id_vehicle_brand": 2, "name": "Mazda"},
                ],
                "models": [
                    {"id_vehicle_model": 1, "name": "2024"},
                    {"id_vehicle_model": 2, "name": "2023"},
                ],
                "colors": [
                    {"id_vehicle_color": 1, "name": "Negro"},
                    {"id_vehicle_color": 1, "name": "Blanco"},
                ],
            },
        ),
    ],
}
