from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
from django.db.models import F, ExpressionWrapper, DateTimeField
from django.utils import timezone
from rest_framework.response import Response
from .serializers import (
    CitySerializer,
    ExtendedUserSerializer,
    UserViewSerializer,
    VehicleColorSerializer,
    VehicleBrandSerializer,
    VehicleTypeSerializer,
    VehicleModelSerializer,
    VehicleSerializer,
    ViewVehicleSerializer,
    TripSerializer,
    ViewTripSerializer,
    ViewPassenger_TripSerializer,
    Passenger_TripSerializer,
    ViewTripForPassengerSerializer,
)
from .models import (
    User,
    City,
    Vehicle,
    VehicleColor,
    VehicleBrand,
    VehicleType,
    VehicleModel,
    Trip,
    Passenger_Trip,
)
from .permissions import IsAdmin, IsDriver, IsPassenger
from api import error_messages
from .schemas import (
    driver_schemas,
    general_schemas,
    registration_schemas,
    user_schemas,
    vehicle_schemas,
)
from djoser.views import UserViewSet

# Admins


# Listar todos los usuarios
@extend_schema(**user_schemas.list_users_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def list_users(request):
    queryset = User.objects.all().order_by('id_user')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    serializer = ExtendedUserSerializer(paginated_results, many=True)
    return paginator.get_paginated_response(serializer.data)


# Vistas de registro


# Obtener datos para el registro
@extend_schema(**registration_schemas.registration_schema)
@api_view(['GET'])
@permission_classes([AllowAny])
def registration(request):
    queryset = City.objects.all()
    serializer = CitySerializer(queryset, many=True)
    content = serializer.data
    return Response(content, status=status.HTTP_200_OK)


# Todos los usuarios
class CustomUserViewSet(UserViewSet):
    @action(['get', 'patch'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)


# Ver perfil
@extend_schema(**user_schemas.get_profile_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    serializer = UserViewSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Conductores


# Mostrar datos en la página de inicio
@extend_schema(**general_schemas.home_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDriver])
def home_driver(request):
    user = request.user
    content = {'name': user.first_name}
    return Response(content, status=status.HTTP_200_OK)


# Obtener datos para registrar un vehículo
@extend_schema(**vehicle_schemas.vehicle_registration_schema)
@api_view(['GET'])
@permission_classes([AllowAny])
def vehicle_registration(request):
    colors = VehicleColor.objects.all()
    colors_serializer = VehicleColorSerializer(colors, many=True)

    brands = VehicleBrand.objects.all()
    brands_serializer = VehicleBrandSerializer(brands, many=True)

    types = VehicleType.objects.all()
    types_serializer = VehicleTypeSerializer(types, many=True)

    models = VehicleModel.objects.all()
    models_serializer = VehicleModelSerializer(models, many=True)

    content = {
        'types': types_serializer.data,
        'brands': brands_serializer.data,
        'models': models_serializer.data,
        'colors': colors_serializer.data,
    }
    return Response(content, status=status.HTTP_200_OK)


# Añadir vehículo
@extend_schema(**driver_schemas.add_vehicle_schema)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDriver])
def add_vehicle(request):
    user = request.user
    vehicle_data = request.data
    '''El dueño debe ser el mismo usuario que realiza la petición.'''
    vehicle_data['owner'] = user.id_user

    vehicle = VehicleSerializer(data=vehicle_data)

    if vehicle.is_valid():
        try:
            vehicle.save()
            return Response(vehicle.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            content = {'error': error_messages.LICENSE_PLATE_ALREADY_EXISTS}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(vehicle.errors, status=status.HTTP_400_BAD_REQUEST)


# Obtener vehículo
@extend_schema(**driver_schemas.get_vehicle_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDriver])
def get_vehicle(request, id_vehicle):
    user = request.user
    try:
        vehicle = Vehicle.objects.get(id_vehicle=id_vehicle, owner=user.id_user)
        serializer = ViewVehicleSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Vehicle.DoesNotExist:
        return Response(
            {'error': error_messages.VEHICLE_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener todos los vehículos
@extend_schema(**driver_schemas.my_vehicles_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDriver])
def my_vehicles(request):
    user = request.user
    vehicles = Vehicle.objects.filter(owner=user.id_user).order_by('license_plate')
    serializer = ViewVehicleSerializer(vehicles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Actualizar vehículo
@extend_schema(**driver_schemas.update_vehicle_schema)
@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated, IsDriver])
def update_vehicle(request, id_vehicle):
    user = request.user
    vehicle_data = request.data

    try:
        vehicle = Vehicle.objects.get(id_vehicle=id_vehicle, owner=user.id_user)
        '''El dueño debe ser el mismo usuario que realiza la petición.'''
        vehicle_data['owner'] = user.id_user
        serializer = VehicleSerializer(vehicle, data=vehicle_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Vehicle.DoesNotExist:
        return Response(
            {'error': error_messages.VEHICLE_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )

    except IntegrityError:
        content = {'error': error_messages.LICENSE_PLATE_ALREADY_EXISTS}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


# Eliminar vehículo
@extend_schema(**driver_schemas.delete_vehicle_schema)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsDriver])
def delete_vehicle(request, id_vehicle):
    user = request.user
    try:
        vehicle = Vehicle.objects.get(id_vehicle=id_vehicle, owner=user.id_user)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Vehicle.DoesNotExist:
        return Response(
            {'error': error_messages.VEHICLE_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Añadir viaje
@extend_schema(**driver_schemas.add_trip_schema)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDriver])
def add_trip(request):
    user = request.user
    trip_data = request.data
    '''El conductor debe ser el mismo usuario que realiza la petición.'''
    trip_data['driver'] = user.id_user

    trip = TripSerializer(data=trip_data)

    if trip.is_valid():
        trip.save()
        return Response(trip.data, status=status.HTTP_201_CREATED)

    else:
        return Response(trip.errors, status=status.HTTP_400_BAD_REQUEST)


# Obtener viaje
@extend_schema(**driver_schemas.get_trip_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDriver])
def get_trip(request, id_trip):
    user = request.user
    try:
        trip = Trip.objects.get(id_trip=id_trip, driver=user.id_user)
        trip_serializer = ViewTripSerializer(trip)

        passengers = Passenger_Trip.objects.filter(trip=id_trip)
        passengers_serializer = ViewPassenger_TripSerializer(passengers, many=True)

        confirmed_passengers = [
            item for item in passengers_serializer.data if item['is_confirmed']
        ]
        pending_passengers = [
            item for item in passengers_serializer.data if not item['is_confirmed']
        ]

        content = trip_serializer.data
        content['confirmed_passengers'] = confirmed_passengers
        content['pending_passengers'] = pending_passengers
        return Response(content, status=status.HTTP_200_OK)

    except Trip.DoesNotExist:
        return Response(
            {'error': error_messages.TRIP_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener historial de viajes
@extend_schema(**driver_schemas.my_vehicles_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDriver])
def trip_history(request):
    user = request.user
    current_datetime = timezone.now()

    queryset = Trip.objects.values(
        'id_trip', 'start_date', 'start_time', 'starting_point', 'arrival_point'
    ).annotate(
        start_datetime=ExpressionWrapper(
            F('start_date') + F('start_time'), output_field=DateTimeField()
        )
    )
    queryset = queryset.filter(
        start_datetime__lt=current_datetime, driver=user.id_user
    ).order_by(
        'start_date', 'start_time'
    )  # lt signifia less than.

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    serializer = TripSerializer(paginated_results, many=True, partial=True)
    return paginator.get_paginated_response(serializer.data)


# Actualizar viaje
@extend_schema(**driver_schemas.update_trip_schema)
@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated, IsDriver])
def update_trip(request, id_trip):
    user = request.user
    trip_data = request.data

    try:
        trip = Trip.objects.get(id_trip=id_trip, driver=user.id_user)
        '''El conductor debe ser el mismo usuario que realiza la petición.'''
        trip_data['driver'] = user.id_user
        serializer = TripSerializer(trip, data=trip_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Trip.DoesNotExist:
        return Response(
            {'error': error_messages.TRIP_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Pasajeros


# Mostrar datos en la página de inicio
@extend_schema(**general_schemas.home_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPassenger])
def home_passenger(request):
    user = request.user
    content = {'name': user.first_name}
    return Response(content, status=status.HTTP_200_OK)


# Obtener viaje
@extend_schema(**driver_schemas.get_trip_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPassenger])
def get_trip_passenger(request, id_trip):
    user = request.user
    try:
        passenger_trip = Passenger_Trip.objects.get(trip=id_trip, passenger=user.id_user)
        passenger_trip_serializer = Passenger_TripSerializer(
            passenger_trip, partial=True
        )

        trip = Trip.objects.get(id_trip=id_trip)
        trip_serializer = ViewTripForPassengerSerializer(trip)

        content = passenger_trip_serializer.data
        content['trip'] = trip_serializer.data
        return Response(content, status=status.HTTP_200_OK)

    except Passenger_Trip.DoesNotExist:
        return Response(
            {'error': error_messages.PASSENGER_IS_NOT_ON_THE_TRIP},
            status=status.HTTP_404_NOT_FOUND,
        )
