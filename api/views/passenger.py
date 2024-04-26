from decimal import Decimal
import requests
from math import sqrt
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.db.models import F, DateTimeField, ExpressionWrapper
from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
from api.serializers.vehicle import ViewVehicleReduceSerializer
from api.serializers.trip import (
    ViewTripSerializer,
    ViewTripMinimalSerializer,
    TripSearchSerializer,
    planned_trips_serializer,
)
from api.serializers.passenger_trip import (
    ViewPassenger_TripReduceSerializer,
    passenger_trip_passenger_serializer,
)
from api.models import Vehicle, Trip, Passenger_Trip
from api.permissions import IsPassenger
from api import error_messages
from api.schemas import passenger_schemas
from api.utils import point_inside_polygon, univalle


# Obtener viaje asociado
@extend_schema(**passenger_schemas.get_trip_associated_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trip_associated(request, id_trip):
    user = request.user
    try:
        passenger_Trip = Passenger_Trip.objects.only(
            'pickup_point_lat',
            'pickup_point_long',
            'seats',
            'is_confirmed',
        ).get(trip=id_trip, passenger=user.id_user)
        passenger_trip_serializer = ViewPassenger_TripReduceSerializer(passenger_Trip)

        trip = (
            Trip.objects.select_related(
                'driver',
            )
            .only(
                'start_date',
                'start_time',
                'starting_point_lat',
                'starting_point_long',
                'arrival_point_lat',
                'arrival_point_long',
                'seats',
                'fare',
                'current_trip',
                'driver__first_name',
                'driver__last_name',
                'driver__phone_number',
                'vehicle',
            )
            .get(id_trip=id_trip)
        )

        trip_serializer = ViewTripSerializer(trip)
        trip_data = trip_serializer.data

        vehicle = (
            Vehicle.objects.select_related(
                'vehicle_type',
                'vehicle_brand',
                'vehicle_model',
                'vehicle_color',
            )
            .only(
                'license_plate',
                'vehicle_type__name',
                'vehicle_brand__name',
                'vehicle_model__name',
                'vehicle_color__name',
            )
            .get(id_vehicle=trip_data['vehicle'])
        )
        vehicle_serializer = ViewVehicleReduceSerializer(vehicle)

        content = passenger_trip_serializer.data
        content['trip'] = trip_data
        content['trip']['vehicle'] = vehicle_serializer.data
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
        trip = (
            Trip.objects.select_related(
                'driver',
            )
            .only(
                'vehicle',
                'driver__first_name',
                'driver__last_name',
                'driver__phone_number',
            )
            .get(id_trip=id_trip)
        )

        trip_serializer = ViewTripMinimalSerializer(trip)
        trip_data = trip_serializer.data

        vehicle = (
            Vehicle.objects.select_related(
                'vehicle_type',
                'vehicle_brand',
                'vehicle_model',
                'vehicle_color',
            )
            .only(
                'license_plate',
                'vehicle_type__name',
                'vehicle_brand__name',
                'vehicle_model__name',
                'vehicle_color__name',
            )
            .get(id_vehicle=trip_data['vehicle'])
        )
        vehicle_serializer = ViewVehicleReduceSerializer(vehicle)

        content = trip_data
        content['vehicle'] = vehicle_serializer.data
        return Response(content, status=status.HTTP_200_OK)

    except Trip.DoesNotExist:
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

    queryset = (
        Passenger_Trip.objects.select_related('trip')
        .only(
            'trip',
            'trip__start_date',
            'trip__start_time',
            'trip__starting_point_lat',
            'trip__starting_point_long',
            'trip__arrival_point_lat',
            'trip__arrival_point_long',
        )
        .annotate(
            start_datetime=ExpressionWrapper(
                F('trip__start_date') + F('trip__start_time'),
                output_field=DateTimeField(),
            )
        )
    )

    queryset = queryset.filter(
        start_datetime__lt=current_datetime, passenger=user.id_user
    ).order_by(
        '-start_datetime'
    )  # lt significa less than.

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    content = [passenger_trip_passenger_serializer(item) for item in paginated_results]
    return paginator.get_paginated_response(content)


# Obtener viajes planeados
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def planned_trips(request):
    user = request.user
    current_datetime = timezone.now()

    queryset = (
        Passenger_Trip.objects.select_related('trip')
        .only(
            'trip',
            'trip__start_date',
            'trip__start_time',
            'trip__starting_point_lat',
            'trip__starting_point_long',
            'trip__arrival_point_lat',
            'trip__arrival_point_long',
        )
        .annotate(
            start_datetime=ExpressionWrapper(
                F('trip__start_date') + F('trip__start_time'),
                output_field=DateTimeField(),
            )
        )
    )

    queryset = queryset.filter(
        start_datetime__gt=current_datetime, passenger=user.id_user
    ).order_by(
        'start_datetime'
    )  # gt significa greater than.

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    content = [passenger_trip_passenger_serializer(item) for item in paginated_results]
    return paginator.get_paginated_response(content)


# Eliminar una reserva
@extend_schema(**passenger_schemas.delete_trip_reservation_schema)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsPassenger])
def delete_trip_reservation(request, id_trip):
    user = request.user
    try:
        passenger_trip = Passenger_Trip.objects.get(
            trip=id_trip, passenger=user.id_user
        )
        passenger_trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Passenger_Trip.DoesNotExist:
        return Response(
            {'error': error_messages.PASSENGER_IS_NOT_ON_THE_TRIP},
            status=status.HTTP_404_NOT_FOUND,
        )


# Buscar viaje
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPassenger])
def search_route(request):
    trip_data = request.data
    errors = {}

    # Parámetros de búsqueda
    trip = TripSearchSerializer(data=trip_data, partial=True)

    # Validaciones
    if trip.is_valid():
        current_datetime = timezone.now()

        start_time = trip_data.get('start_time', None)

        # Si no se proporciona fecha u hora, se asigna la hora o la fecha actual.
        if start_time:
            start_time = datetime.strptime(start_time, '%H:%M:%S').time()
        else:
            start_time = current_datetime.time()

        start_date = trip_data.get('start_date', None)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = current_datetime.date()

        start_datetime = datetime.combine(start_date, start_time)

        seats = trip_data.get('seats', 1)

        starting_point_lat = trip_data['starting_point_lat']
        starting_point_long = trip_data['starting_point_long']
        arrival_point_lat = trip_data['arrival_point_lat']
        arrival_point_long = trip_data['arrival_point_long']

        # Se determina si Univalle es el punto de inicio o de destino.
        starting_point = [
            Decimal(f'{starting_point_long}'),
            Decimal(f'{starting_point_lat}'),
        ]

        arrival_point = [
            Decimal(f'{arrival_point_long}'),
            Decimal(f'{arrival_point_lat}'),
        ]

        comes_from_the_u = point_inside_polygon(starting_point, univalle)
        goes_to_the_u = point_inside_polygon(arrival_point, univalle)

        direction = ''

        if goes_to_the_u:
            direction = 'Va para la u'

        if comes_from_the_u:
            direction = 'Viene de la u'

        if not comes_from_the_u and not goes_to_the_u:
            errors['error'] = error_messages.PASSENGER_MUST_GO_TO_OR_COME_FROM_UV

    errors = {**trip.errors, **errors}

    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    queryset = (
        Trip.objects.only(
            'id_trip',
            'start_date',
            'start_time',
            'starting_point_lat',
            'starting_point_long',
            'arrival_point_lat',
            'arrival_point_long',
            'seats',
            'fare',
        )
        .annotate(
            start_datetime=ExpressionWrapper(
                F('start_date') + F('start_time'), output_field=DateTimeField()
            )
        )
        .filter(start_datetime__gte=start_datetime, seats__gte=seats)
        .order_by('start_datetime')
    )  # gte significa greater than equal.

    content = [
        {
            'count': queryset.count(),
            'direction': direction,
            'results': [planned_trips_serializer(item) for item in queryset],
        }
    ]
    return Response(content, status=status.HTTP_200_OK)

''' 
    starting_point = [
        Decimal(f'{-76.537502}'),
        Decimal(f'{3.380173}'),
    ]

    isUnivalle = point_inside_polygon(starting_point, univalle)

    
    MAPBOX_KEY = settings.MAPBOX_KEY

    starting_point_lat = trip_data['starting_point_lat']
    starting_point_long = trip_data['starting_point_long']
    arrival_point_lat = trip_data['arrival_point_lat']
    arrival_point_long = trip_data['arrival_point_long']

    url = (
        'https://api.mapbox.com/directions/v5/mapbox/driving/'
        + f'{starting_point_long},{starting_point_lat};'
        + f'{arrival_point_long},{arrival_point_lat}/'
        + '?geometries=geojson&language=es&access_token='
        + MAPBOX_KEY
    )

    response = requests.get(url)
    data = response.json()

    routes = data.get('routes', None)

    if routes:
        # Si se encontraron rutas, devolver la primera ruta.
        route = routes[0]['geometry']['coordinates']

        # Cálculo de la distancia entre dos puntos:
        # raiz( (x2-x1)^2 + (y2-y1)^2 )
        for point in route:
            x_distance = (
                Decimal(f'{pickup_point_long}') - Decimal(f'{point[0]}')
            ) ** 2
            y_distance = (
                Decimal(f'{pickup_point_lat}') - Decimal(f'{point[1]}')
            ) ** 2
            suma = Decimal(f'{x_distance}') + Decimal(f'{y_distance}')
            distance = sqrt(Decimal(f'{suma}'))

            point.append(Decimal(f'{distance}'))

        return Response(
            {'ruta': route, 'va para la U': isUnivalle}, status=status.HTTP_200_OK
        )
    else:
        message = data.get('message', None)
        error = message if message else error_messages.NO_ROUTE_FOUND
        return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)
'''
