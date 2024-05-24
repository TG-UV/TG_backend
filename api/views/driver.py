from functools import partial
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError, transaction
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from api.serializers.vehicle import (
    ViewVehicleSerializer,
    VehicleSerializerNoValidation,
)
from api.serializers.trip import (
    TripSerializer,
    planned_trips_serializer,
    trip_reduce_serializer,
    ViewTripReduceSerializer,
)
from api.serializers.passenger_trip import ViewPassenger_TripSerializer
from api.models import Vehicle, Trip, Passenger_Trip, Device
from api.permissions import IsDriver
from api import error_messages
from api.schemas import driver_schemas
from .notification import (
    send_trip_canceled,
    send_reservation_accepted,
    send_reservation_rejected,
)


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
        vehicle = Vehicle.objects.get_my_vehicle(id_vehicle, user.id_user)
        serializer = ViewVehicleSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Vehicle.DoesNotExist:
        return Response(
            {'error': error_messages.VEHICLE_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener todos los vehículos
@extend_schema(**driver_schemas.get_my_vehicles_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_vehicles(request):
    user = request.user
    vehicles = Vehicle.objects.get_my_vehicles(user.id_user)
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
        vehicle = Vehicle.objects.only('id_vehicle').get(
            id_vehicle=id_vehicle, owner=user.id_user
        )
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
        try:
            trip.save()
            return Response(trip.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            content = {'error': error_messages.TRIP_ALREADY_EXISTS}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

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
        queryset = Passenger_Trip.objects.get_passengers(id_trip)
        serializer = ViewPassenger_TripSerializer(queryset, many=True)
        content = {'id_trip': id_trip, 'passengers': serializer.data}
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': error_messages.TRIP_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener viajes de un queryset dado
def get_trips(request, queryset, serializer):
    user = request.user
    current_datetime = timezone.now()
    queryset = queryset(current_datetime, user.id_user)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    content = [serializer(item) for item in paginated_results]
    return paginator.get_paginated_response(content)


# Obtener historial de viajes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trip_history(request):
    queryset = Trip.objects.get_trip_history
    serializer = trip_reduce_serializer
    return get_trips(request, queryset, serializer)


# Obtener viajes planeados
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_planned_trips(request):
    queryset = Trip.objects.get_planned_trips
    serializer = planned_trips_serializer
    return get_trips(request, queryset, serializer)


# Obtener viaje actual
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_trip(request):
    user = request.user
    current_datetime = timezone.now()
    two_hours_ago_datetime = timezone.now() - timedelta(hours=2)
    queryset = Trip.objects.get_current_trip(
        current_datetime, two_hours_ago_datetime, user.id_user
    )
    content = trip_reduce_serializer(queryset) if queryset else {}
    return Response(content, status=status.HTTP_200_OK)


# Eliminar viaje
@extend_schema(**driver_schemas.delete_trip_schema)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsDriver])
def delete_trip(request, id_trip):
    user = request.user
    try:
        with transaction.atomic():

            trip = Trip.objects.get_my_trip(id_trip, driver=user.id_user)
            trip_data = ViewTripReduceSerializer(trip).data

            # Enviar notificación a los pasajeros.
            devices = Device.objects.filter(
                user__passenger_trip__trip_id=id_trip
            ).values_list('id_device', flat=True)
            devices = list(devices)

            trip.delete()

            if devices:
                transaction.on_commit(
                    partial(send_trip_canceled, devices, trip_data)
                )

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Trip.DoesNotExist:
        return Response(
            {'error': error_messages.TRIP_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Confirmar reserva hecha por un pasajero
# @extend_schema(**driver_schemas.delete_passenger_trip_schema)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDriver])
def confirm_passenger_trip(request, id_passenger_trip):
    user = request.user
    try:
        passenger_trip_query = Passenger_Trip.objects.get_basic_reservation_info(
            id_passenger_trip, user.id_user
        )

        if passenger_trip_query.is_confirmed:
            return Response(
                {'error': error_messages.RESERVATION_ALREADY_CONFIRMED},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if passenger_trip_query.trip.seats >= passenger_trip_query.seats:
            with transaction.atomic():
                trip = (
                    Trip.objects.select_for_update()
                    .only('seats')
                    .get(id_trip=passenger_trip_query.trip_id)
                )

                passenger_trip = (
                    Passenger_Trip.objects.select_for_update()
                    .only('is_confirmed')
                    .get(id_passenger_trip=id_passenger_trip)
                )

                trip.seats -= passenger_trip_query.seats
                trip.save(update_fields=['seats'])

                passenger_trip.is_confirmed = True
                passenger_trip.save(update_fields=['is_confirmed'])

                # Enviar notificación al pasajero.
                devices = Device.objects.filter(
                    user__passenger_trip=id_passenger_trip
                ).values_list('id_device', flat=True)
                devices = list(devices)

                if devices:
                    transaction.on_commit(
                        partial(
                            send_reservation_accepted,
                            devices,
                            passenger_trip_query.trip_id,
                        )
                    )

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(
                {'error': error_messages.NOT_ENOUGH_SEATS},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Passenger_Trip.DoesNotExist:
        return Response(
            {'error': error_messages.RESERVATION_NOT_FOUND},
            status=status.HTTP_404_NOT_FOUND,
        )


# Descartar reserva hecha por un pasajero
@extend_schema(**driver_schemas.delete_passenger_trip_schema)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsDriver])
def delete_passenger_trip(request, id_passenger_trip):
    user = request.user
    try:
        passenger_trip = Passenger_Trip.objects.get_data_to_delete_reservation(
            id_passenger_trip, user.id_user
        )
        id_trip = passenger_trip.trip_id

        with transaction.atomic():
            # Si la reserva ya estaba confirmada se restablecen los puestos separados.
            if passenger_trip.is_confirmed:
                trip = (
                    Trip.objects.select_for_update()
                    .only('seats')
                    .get(id_trip=id_trip)
                )
                trip.seats += passenger_trip.seats
                trip.save(update_fields=['seats'])

            # Enviar notificación al pasajero.
            devices = Device.objects.filter(
                user__passenger_trip=id_passenger_trip
            ).values_list('id_device', flat=True)
            devices = list(devices)

            passenger_trip.delete()

            if devices:
                transaction.on_commit(
                    partial(
                        send_reservation_rejected,
                        devices,
                        id_trip,
                    )
                )

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Passenger_Trip.DoesNotExist:
        return Response(
            {'error': error_messages.RESERVATION_NOT_FOUND},
            status=status.HTTP_404_NOT_FOUND,
        )
