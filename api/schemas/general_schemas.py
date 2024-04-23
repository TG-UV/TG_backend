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


get_profile_schema = {
    'description': 'Datos del usuario que realiza la petición (requiere token).',
    'responses': {
        200: inline_serializer(
            name="UserProfile",
            fields={
                "id_user": serializers.IntegerField(),
                "email": serializers.EmailField(),
                "identity_document": serializers.CharField(),
                "phone_number": serializers.CharField(),
                "first_name": serializers.CharField(),
                "last_name": serializers.CharField(),
                "date_of_birth": serializers.DateField(),
                "residence_city": serializers.CharField(),
                "type": serializers.CharField(),
                "is_active": serializers.BooleanField(),
            },
        ),
    },
    'examples': [
        OpenApiExample(
            "User profile",
            value={
                "id_user": 9,
                "email": "sofi@gmail.com",
                "identity_document": "12345",
                "phone_number": "3204656678",
                "first_name": "Sofia",
                "last_name": "Ríos",
                "date_of_birth": "2000-10-22",
                "residence_city": "Cali",
                "type": "Pasajero",
                "is_active": True,
            },
            description='Se reemplazan los ids por los nombres de los campos. Por ej. '
            + 'en "residence_city" aparece "Cali" en vez del id 1.',
        ),
    ],
}
