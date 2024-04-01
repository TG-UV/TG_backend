from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, inline_serializer

home_schema = {
    'description': 'Datos para la página de inicio de un usuario (requiere token).',
    'responses': {
        200: inline_serializer(
            name="Home",
            fields={
                "name": serializers.CharField(),
            },
        ),
    },
    'examples': [
        OpenApiExample(
            "Home",
            value={"name": "Camila"},
            status_codes=['200'],
        ),
    ],
}
