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
