from drf_spectacular.utils import OpenApiExample
from api.serializers.user import ExtendedUserSerializer

list_users_schema = {
    'description': 'Lista de usuarios registrados en la aplicación (requiere token).',
    'responses': {
        200: ExtendedUserSerializer,
    },
    'examples': [
        OpenApiExample(
            "User list",
            value={
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id_user": 3,
                        "email": "javier@correo.com",
                        "identity_document": "44444",
                        "phone_number": "3224224444",
                        "first_name": "Javier",
                        "last_name": "Jr",
                        "date_of_birth": "2000-02-14",
                        "registration_date": "2024-01-16T11:39:58.230409",
                        "residence_city": 1,
                        "type": 2,
                        "last_login": "2024-03-15T22:56:51.294556",
                        "is_active": True,
                        "is_staff": False,
                        "is_superuser": False,
                    },
                    {
                        "id_user": 4,
                        "email": "david@gmail.com",
                        "identity_document": "11111",
                        "phone_number": "3204654444",
                        "first_name": "David",
                        "last_name": "Gray",
                        "date_of_birth": "2001-04-10",
                        "registration_date": "2024-01-18T21:00:01.850562",
                        "residence_city": 2,
                        "type": 2,
                        "last_login": "2024-03-10T18:28:45.078639",
                        "is_active": True,
                        "is_staff": False,
                        "is_superuser": False,
                    },
                ],
            },
            description='En este ejemplo solo hay 2 usuarios registrados por lo que '
            + 'no existen enlaces para mostrar más usuarios.',
        ),
    ],
}
