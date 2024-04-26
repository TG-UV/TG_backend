from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
from django.db.models import F, DateTimeField, ExpressionWrapper
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from api.serializers.vehicle import (
    ViewVehicleSerializer,
    VehicleSerializerNoValidation,
)
from api.serializers.trip import (
    TripSerializer,
    ViewTripReduceSerializer,
    planned_trips_serializer,
)
from api.serializers.passenger_trip import ViewPassenger_TripSerializer
from api.models import Vehicle, Trip, Passenger_Trip
from api.permissions import IsDriver
from api import error_messages
from api.schemas import driver_schemas


# Añadir vehículo
@extend_schema(**driver_schemas.add_vehicle_schema)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDriver])
def add_vehicle(request):
    user = request.user
    vehicle_data = request.data
    '''El dueño debe ser el mismo usuario que realiza la petición.'''
    vehicle_data['owner'] = user.id_user

    vehicle = VehicleSerializerNoValidation(data=vehicle_data)

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
@permission_classes([IsAuthenticated])
def get_vehicle(request, id_vehicle):
    user = request.user
    try:
        vehicle = (
            Vehicle.objects.select_related(
                'vehicle_type',
                'vehicle_brand',
                'vehicle_model',
                'vehicle_color',
            )
            .only(
                'id_vehicle',
                'vehicle_type',
                'vehicle_brand',
                'vehicle_model',
                'vehicle_color',
                'license_plate',
            )
            .get(id_vehicle=id_vehicle, owner=user.id_user)
        )
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
@permission_classes([IsAuthenticated])
def my_vehicles(request):
    user = request.user
    vehicles = (
        Vehicle.objects.filter(owner=user.id_user)
        .select_related(
            'vehicle_type',
            'vehicle_brand',
            'vehicle_model',
            'vehicle_color',
        )
        .only(
            'id_vehicle',
            'vehicle_type',
            'vehicle_brand',
            'vehicle_model',
            'vehicle_color',
            'license_plate',
        )
        .order_by('license_plate')
    )
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

        '''Si el método es PUT debe tener todos los campos.'''
        partial = False if request.method == 'PUT' else True

        serializer = VehicleSerializerNoValidation(
            vehicle, data=vehicle_data, partial=partial
        )

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
@permission_classes([IsAuthenticated])
def get_trip(request, id_trip):
    user = request.user
    trip = Trip.objects.filter(id_trip=id_trip, driver=user.id_user).exists()

    if trip:
        queryset = (
            Passenger_Trip.objects.filter(trip=id_trip)
            .select_related(
                'passenger',
            )
            .only(
                'passenger',
                'pickup_point_lat',
                'pickup_point_long',
                'seats',
                'is_confirmed',
                'passenger__phone_number',
                'passenger__first_name',
                'passenger__last_name',
            )
        )
        serializer = ViewPassenger_TripSerializer(queryset, many=True)
        content = {'id_trip': id_trip, 'passengers': serializer.data}
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': error_messages.TRIP_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener historial de viajes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trip_history(request):
    user = request.user
    current_datetime = timezone.now()

    queryset = Trip.objects.only(
        'id_trip',
        'start_date',
        'start_time',
        'starting_point_lat',
        'starting_point_long',
        'arrival_point_lat',
        'arrival_point_long',
    ).annotate(
        start_datetime=ExpressionWrapper(
            F('start_date') + F('start_time'), output_field=DateTimeField()
        )
    )

    queryset = queryset.filter(
        start_datetime__lt=current_datetime, driver=user.id_user
    ).order_by(
        '-start_datetime'
    )  # lt significa less than.

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    serializer = ViewTripReduceSerializer(paginated_results, many=True)
    return paginator.get_paginated_response(serializer.data)


# Obtener viajes planeados
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def planned_trips(request):
    user = request.user
    current_datetime = timezone.now()

    queryset = Trip.objects.only(
        'id_trip',
        'start_date',
        'start_time',
        'starting_point_lat',
        'starting_point_long',
        'arrival_point_lat',
        'arrival_point_long',
        'seats',
        'fare',
    ).annotate(
        start_datetime=ExpressionWrapper(
            F('start_date') + F('start_time'), output_field=DateTimeField()
        )
    )

    queryset = queryset.filter(
        start_datetime__gt=current_datetime, driver=user.id_user
    ).order_by(
        'start_datetime'
    )  # gt significa greater than.

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    content = [planned_trips_serializer(item) for item in paginated_results]
    return paginator.get_paginated_response(content)


# Obtener viaje actual
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_trip(request):
    user = request.user
    current_datetime = timezone.now()
    two_hours_ago = timezone.now() - timedelta(hours=2)

    queryset = Trip.objects.only(
        'id_trip',
        'start_date',
        'start_time',
        'starting_point_lat',
        'starting_point_long',
        'arrival_point_lat',
        'arrival_point_long',
    ).annotate(
        start_datetime=ExpressionWrapper(
            F('start_date') + F('start_time'), output_field=DateTimeField()
        )
    )

    queryset = (
        queryset.filter(
            start_datetime__lte=current_datetime,
            start_datetime__gt=two_hours_ago,
            driver=user.id_user,
        )
        .order_by('-start_datetime')
        .first()
    )  # lte significa less than equal.

    serializer = ViewTripReduceSerializer(queryset)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Eliminar viaje
@extend_schema(**driver_schemas.delete_trip_schema)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsDriver])
def delete_trip(request, id_trip):
    user = request.user
    try:
        trip = Trip.objects.get(id_trip=id_trip, driver=user.id_user)
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Trip.DoesNotExist:
        return Response(
            {'error': error_messages.TRIP_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )
