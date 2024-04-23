from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.db.models import F, DateTimeField, ExpressionWrapper
from django.utils import timezone
from rest_framework.response import Response
from api.serializers.vehicle import ViewVehicleReduceSerializer
from api.serializers.trip import (
    ViewTripSerializer,
    ViewTripMinimalSerializer,
)
from api.serializers.passenger_trip import (
    ViewPassenger_TripReduceSerializer,
    passenger_trip_passenger_serializer,
)
from api.models import Vehicle, Trip, Passenger_Trip
from api.permissions import IsPassenger
from api import error_messages
from api.schemas import passenger_schemas


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
    )  # lt signifia less than.

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
    )  # gt signifia greater than.

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    content = [passenger_trip_passenger_serializer(item) for item in paginated_results]
    return paginator.get_paginated_response(content)
