from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.response import Response
from .serializers import UserCustomSerializer, CitySerializer, VehicleSerializer
from .models import User, City, Vehicle
from .permissions import IsAdmin, IsDriver, IsPassenger

# Admins


# Listar todos los usuarios
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def list_users(request):
    queryset = User.objects.all()
    serializer = UserCustomSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Vistas de registro


# Obtener datos para el registro
@api_view(['GET'])
@permission_classes([AllowAny])
def registration(request):
    queryset = City.objects.all()
    serializer = CitySerializer(queryset, many=True)
    content = serializer.data
    return Response(content, status=status.HTTP_200_OK)


# Conductores


# Añadir vehículo
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDriver])
def add_vehicle(request):
    user = request.user
    vehicle_data = request.data
    vehicle_data['owner'] = (
        user.id_user
    )  # El dueño es el mismo usuario que realiza la petición.
    vehicle = VehicleSerializer(data=vehicle_data)

    if vehicle.is_valid():
        try:
            vehicle.save()
            return Response(vehicle.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            content = {'error': 'Ya tienes un vehículo con esa placa.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(vehicle.errors, status=status.HTTP_400_BAD_REQUEST)


# Obtener vehículo
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDriver])
def get_vehicle(request, id):
    user = request.user
    try:
        queryset = Vehicle.objects.get(id_vehicle=id)

        if queryset.owner.id_user == user.id_user:
            serializer = VehicleSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(
                {'error': 'Acceso no autorizado.'},
                status=status.HTTP_403_FORBIDDEN,
            )

    except Vehicle.DoesNotExist:
        return Response(
            {'error': 'No se encontró un vehículo con ese id.'},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Obtener todos los vehículos
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDriver])
def my_vehicles(request):
    user = request.user
    queryset = Vehicle.objects.filter(owner=user.id_user)
    serializer = VehicleSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Mostrar datos en la página de inicio
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDriver])
def home_driver(request):
    user = request.user
    content = {'name': user.first_name}
    return Response(content, status=status.HTTP_200_OK)


# Pasajeros


# Mostrar datos en la página de inicio
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPassenger])
def home_passenger(request):
    user = request.user
    content = {'name': user.first_name}
    return Response(content, status=status.HTTP_200_OK)
