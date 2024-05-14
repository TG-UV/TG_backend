from functools import partial
from decimal import Decimal, localcontext
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework.response import Response
from api.serializers.trip import (
    ViewTripSerializer,
    ViewTripMinimalSerializer,
    TripSearchSerializer,
    planned_trips_serializer,
    trip_reduce_serializer,
)
from api.serializers.passenger_trip import (
    Passenger_TripSerializer,
    ViewPassenger_TripReduceSerializer,
)
from api.models import Trip, Passenger_Trip, Device
from api.permissions import IsPassenger
from api import error_messages
from api.schemas import passenger_schemas
from api.utils import point_inside_polygon, univalle, distance, convert_to_decimal_list
from .notification import send_new_reservation, send_reservation_canceled


# Obtener viaje asociado
@extend_schema(**passenger_schemas.get_trip_associated_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trip_associated(request, id_trip):
    user = request.user
    try:
        passenger_Trip = Passenger_Trip.objects.get_reservation(id_trip, user.id_user)
        passenger_trip_serializer = ViewPassenger_TripReduceSerializer(passenger_Trip)

        trip = Trip.objects.get_trip_with_driver_and_vehicle(id_trip)
        trip_serializer = ViewTripSerializer(trip)
        content = passenger_trip_serializer.data
        content['trip'] = trip_serializer.data
        return Response(content, status=status.HTTP_200_OK)

    except Passenger_Trip.DoesNotExist:
        return Response(
            {'error': error_messages.PASSENGER_IS_NOT_ON_THE_TRIP},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener viaje
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trip(request, id_trip):
    try:
        trip = Trip.objects.get_driver_and_vehicle_from_trip(id_trip)
        trip_serializer = ViewTripMinimalSerializer(trip)
        return Response(trip_serializer.data, status=status.HTTP_200_OK)

    except Trip.DoesNotExist:
        return Response(
            {'error': error_messages.TRIP_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener viajes de un queryset dado
def get_trips(request, queryset):
    user = request.user
    current_datetime = timezone.now()
    queryset = queryset(current_datetime, user.id_user)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    content = [trip_reduce_serializer(item.trip) for item in paginated_results]
    return paginator.get_paginated_response(content)


# Obtener historial de viajes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trip_history(request):
    queryset = Passenger_Trip.objects.get_trip_history
    return get_trips(request, queryset)


# Obtener viajes planeados
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def planned_trips(request):
    queryset = Passenger_Trip.objects.get_planned_trips
    return get_trips(request, queryset)


# Reservar un viaje
@extend_schema(**passenger_schemas.book_trip_schema)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPassenger])
def book_trip(request):
    user = request.user
    passenger_trip_data = request.data
    '''El pasajero debe ser el mismo usuario que realiza la petición.'''
    passenger_trip_data['passenger'] = user.id_user
    passenger_trip_data['is_confirmed'] = False

    passenger_trip = Passenger_TripSerializer(data=passenger_trip_data)

    if passenger_trip.is_valid():
        try:
            with transaction.atomic():
                passenger_trip.save()

                # Enviar notificación al conductor.
                id_trip = passenger_trip_data['trip']
                devices = Device.objects.filter(user__trip=id_trip).values_list(
                    'id_device', flat=True
                )

                devices = list(devices)

                if devices:
                    transaction.on_commit(
                        partial(send_new_reservation, devices, id_trip)
                    )

            return Response(passenger_trip.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            content = {'error': error_messages.PASSENGER_HAS_ALREADY_BOOKED}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(passenger_trip.errors, status=status.HTTP_400_BAD_REQUEST)


# Eliminar una reserva
@extend_schema(**passenger_schemas.delete_trip_reservation_schema)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsPassenger])
def delete_trip_reservation(request, id_trip):
    user = request.user
    try:
        passenger_trip = Passenger_Trip.objects.only('seats', 'is_confirmed').get(
            trip=id_trip, passenger=user.id_user
        )

        with transaction.atomic():
            # Si la reserva ya estaba confirmada se restablecen los puestos separados.
            if passenger_trip.is_confirmed:
                trip = (
                    Trip.objects.select_for_update().only('seats').get(id_trip=id_trip)
                )
                trip.seats += passenger_trip.seats
                trip.save(update_fields=['seats'])

            passenger_trip.delete()

            # Enviar notificación al conductor.
            devices = Device.objects.filter(user__trip=id_trip).values_list(
                'id_device', flat=True
            )
            devices = list(devices)

            if devices:
                transaction.on_commit(
                    partial(send_reservation_canceled, devices, id_trip)
                )

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Passenger_Trip.DoesNotExist:
        return Response(
            {'error': error_messages.PASSENGER_IS_NOT_ON_THE_TRIP},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener ruta de Mapbox
def get_route(starting_point, arrival_point):
    MAPBOX_KEY = settings.MAPBOX_KEY

    url = (
        'https://api.mapbox.com/directions/v5/mapbox/driving/'
        + f'{starting_point[0]},{starting_point[1]};'
        + f'{arrival_point[0]},{arrival_point[1]}/'
        + '?geometries=geojson&language=es&access_token='
        + MAPBOX_KEY
    )

    response = requests.get(url)
    data = response.json()
    routes = data.get('routes', None)

    if routes:
        return routes[0]['geometry']['coordinates']

    return [starting_point, arrival_point]


# Compara cada punto de una ruta para hallar el más cercano a un punto dado
def calculate_nearest_point(trip, point_to_compare):
    starting_point = convert_to_decimal_list(
        trip.starting_point_long, trip.starting_point_lat
    )

    arrival_point = convert_to_decimal_list(
        trip.arrival_point_long, trip.arrival_point_lat
    )

    route = get_route(starting_point, arrival_point)

    for point in route:
        # Establece 4 dígitos de precisión para los cálculos de distancia.
        with localcontext() as ctx:
            ctx.prec = 4
            distance_between = distance(point_to_compare, point)
            point.append(Decimal(f'{distance_between}'))

    minimum = min(route, key=lambda x: x[2])  # route = [long, lat, distance]
    trip_serializer = planned_trips_serializer(trip)
    trip_serializer['closest_point'] = minimum
    # trip_serializer['ruta'] = route
    return trip_serializer


# Buscar viaje
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_route(request):
    trip_data = request.data

    # Parámetros de búsqueda.
    trip = TripSearchSerializer(data=trip_data, partial=True)

    # Validaciones.
    if trip.is_valid():
        current_datetime = timezone.now()

        start_time = trip_data.get('start_time', current_datetime.time())
        start_date = trip_data.get('start_date', current_datetime.date())
        seats = trip_data.get('seats', 1)

        starting_point_lat = trip_data['starting_point_lat']
        starting_point_long = trip_data['starting_point_long']
        arrival_point_lat = trip_data['arrival_point_lat']
        arrival_point_long = trip_data['arrival_point_long']

        # Se determina si Univalle es el punto de inicio o de destino.
        starting_point_search = convert_to_decimal_list(
            starting_point_long, starting_point_lat
        )

        arrival_point_search = convert_to_decimal_list(
            arrival_point_long, arrival_point_lat
        )

        comes_from_the_u = point_inside_polygon(starting_point_search, univalle)
        goes_to_the_u = point_inside_polygon(arrival_point_search, univalle)

        if not comes_from_the_u and not goes_to_the_u:
            return Response(
                {'error': error_messages.PASSENGER_MUST_GO_TO_OR_COME_FROM_UV},
                status=status.HTTP_400_BAD_REQUEST,
            )

    else:
        return Response(trip.errors, status=status.HTTP_400_BAD_REQUEST)

    queryset = Trip.objects.search_trips(start_date, start_time, seats)

    results = []
    direction = ''

    if goes_to_the_u:
        # Selecciona aquellos viajes que van a la universidad.
        direction = 'Viajes hacia la universidad'

        for item in queryset:
            arrival_point = convert_to_decimal_list(
                item.arrival_point_long, item.arrival_point_lat
            )

            # Comprueba si el destino del viaje es la universidad.
            if point_inside_polygon(arrival_point, univalle):
                trip = calculate_nearest_point(item, starting_point_search)
                results.append(trip)

    else:
        # Selecciona aquellos viajes que salen de la universidad.
        direction = 'Viajes desde la universidad'

        for item in queryset:
            starting_point = convert_to_decimal_list(
                item.starting_point_long, item.starting_point_lat
            )

            # Comprueba si el origen del viaje es la universidad.
            if point_inside_polygon(starting_point, univalle):
                trip = calculate_nearest_point(item, arrival_point_search)
                results.append(trip)

    sorted_results = (
        sorted(results, key=lambda x: x['closest_point'][2]) if results else []
    )

    content = [
        {
            'count': len(results),
            'direction': direction,
            'results': sorted_results,
        }
    ]

    return Response(content, status=status.HTTP_200_OK)
