from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
def signin(request):
    email = request.POST['email']
    password = request.POST['password']

    if email and password:
        user = authenticate(request, email=email, password=password)

        if user is None:
            return JsonResponse(
                {'error': 'correo o contraseña incorrecta'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            login(request, user)
            return JsonResponse(
                {'mensaje': 'Sesión iniciada'}, status=status.HTTP_200_OK
            )

    else:
        return JsonResponse(
            {'error': 'los campos de correo y contraseña son requeridos'},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hello_view(request):
    content = {
        'message': 'Hello, World!',
        'user': str(request.user), 
        'auth': str(request.auth),
    }
    return Response(content)
