from decimal import Decimal, localcontext
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
from django.db.models import F, DateTimeField, ExpressionWrapper
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
    Passenger_TripSerializer,
    ViewPassenger_TripReduceSerializer,
    passenger_trip_passenger_serializer,
)
from api.models import Vehicle, Trip, Passenger_Trip
from api.permissions import IsPassenger
from api import error_messages
from api.schemas import passenger_schemas
from api.utils import point_inside_polygon, univalle, distance


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


# Reservar un viaje
@extend_schema(**passenger_schemas.book_trip_schema)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPassenger])
def book_trip(request):
    user = request.user
    passenger_trip_data = request.data
    '''El pasajero debe ser el mismo usuario que realiza la petición.'''
    passenger_trip_data['passenger'] = user.id_user

    passenger_trip = Passenger_TripSerializer(data=passenger_trip_data)

    if passenger_trip.is_valid():
        try:
            passenger_trip.save()
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

        # Si la reserva ya estaba confirmada se restablecen los puestos separados.
        if passenger_trip.is_confirmed:
            trip = Trip.objects.filter(id_trip=id_trip)
            trip.update(seats=F('seats') + passenger_trip.seats)

        passenger_trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Passenger_Trip.DoesNotExist:
        return Response(
            {'error': error_messages.PASSENGER_IS_NOT_ON_THE_TRIP},
            status=status.HTTP_404_NOT_FOUND,
        )


# Buscar viaje
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_route(request):
    trip_data = request.data
    errors = {}

    # Parámetros de búsqueda.
    trip = TripSearchSerializer(data=trip_data, partial=True)

    # Validaciones.
    if trip.is_valid():
        current_datetime = timezone.now()

        # Si no se proporciona fecha, hora o puestos, se asignan valores por defecto.
        start_time = trip_data.get('start_time', current_datetime.time())
        start_date = trip_data.get('start_date', current_datetime.date())
        seats = trip_data.get('seats', 1)

        starting_point_lat = trip_data['starting_point_lat']
        starting_point_long = trip_data['starting_point_long']
        arrival_point_lat = trip_data['arrival_point_lat']
        arrival_point_long = trip_data['arrival_point_long']

        # Se determina si Univalle es el punto de inicio o de destino.
        starting_point_search = [
            Decimal(f'{starting_point_long}'),
            Decimal(f'{starting_point_lat}'),
        ]

        arrival_point_search = [
            Decimal(f'{arrival_point_long}'),
            Decimal(f'{arrival_point_lat}'),
        ]

        comes_from_the_u = point_inside_polygon(starting_point_search, univalle)
        goes_to_the_u = point_inside_polygon(arrival_point_search, univalle)

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
        .filter(start_date=start_date, start_time__gte=start_time, seats__gte=seats)
        .order_by('start_time')
    )  # gte significa greater than equal.

    results = []
    direction = ''

    if goes_to_the_u:
        # Selecciona aquellos viajes que van a la universidad
        direction = 'Viajes hacia la universidad'

        for item in queryset:
            if point_inside_polygon(
                [item.arrival_point_long, item.arrival_point_lat], univalle
            ):
                starting_point = [
                    Decimal(f'{item.starting_point_long}'),
                    Decimal(f'{item.starting_point_lat}'),
                ]

                arrival_point = [
                    Decimal(f'{item.arrival_point_long}'),
                    Decimal(f'{item.arrival_point_lat}'),
                ]

                route = get_route(starting_point, arrival_point)

                for point in route:
                    # Establece 4 dígitos de precisión para los cálculos de distancia.
                    with localcontext() as ctx:
                        ctx.prec = 4
                        distance_between = distance(starting_point_search, point)
                        point.append(Decimal(f'{distance_between}'))

                minimum = min(route, key=lambda x: x[2])
                trip_serializer = planned_trips_serializer(item)
                trip_serializer['closest_point'] = minimum
                # trip_serializer['ruta'] = route
                results.append(trip_serializer)

    else:
        # Selecciona aquellos viajes que salen desde la universidad
        direction = 'Viajes desde la universidad'

        for item in queryset:
            if point_inside_polygon(
                [item.starting_point_long, item.starting_point_lat], univalle
            ):
                starting_point = [
                    Decimal(f'{item.starting_point_long}'),
                    Decimal(f'{item.starting_point_lat}'),
                ]

                arrival_point = [
                    Decimal(f'{item.arrival_point_long}'),
                    Decimal(f'{item.arrival_point_lat}'),
                ]

                route = get_route(starting_point, arrival_point)

                for point in route:
                    # Establece 4 dígitos de precisión para los cálculos de distancia.
                    with localcontext() as ctx:
                        ctx.prec = 4
                        distance_between = distance(arrival_point_search, point)
                        point.append(Decimal(f'{distance_between}'))

                minimum = min(route, key=lambda x: x[2])
                trip_serializer = planned_trips_serializer(item)
                trip_serializer['closest_point'] = minimum
                # trip_serializer['ruta'] = route
                results.append(trip_serializer)

    sorted_results = []

    if results:
        sorted_results = sorted(results, key=lambda x: x['closest_point'][2])

    content = [
        {
            'count': len(results),
            'direction': direction,
            'results': sorted_results,
        }
    ]

    return Response(content, status=status.HTTP_200_OK)


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
        # Si se encontraron rutas, devolver la primera ruta.
        route = routes[0]['geometry']['coordinates']
        return route
    else:
        return []
