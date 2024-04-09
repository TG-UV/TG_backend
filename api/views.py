from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
from django.db.models import F, DateTimeField, ExpressionWrapper
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from .serializers import (
    CitySerializer,
    ExtendedUserSerializer,
    ViewUserSerializer,
    VehicleColorSerializer,
    VehicleBrandSerializer,
    VehicleTypeSerializer,
    VehicleModelSerializer,
    ViewVehicleSerializer,
    ViewVehicleSerializerForPassenger,
    TripSerializer,
    ViewTripReduceSerializer,
    VehicleSerializerForDriver,
    ViewPassenger_TripSerializerForDriver,
    ViewPassenger_TripSerializerForPassenger,
    ViewTripSerializer,
    ViewTripDriverSerializer,
    serialize_passenger_trip,
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
from .permissions import IsAdmin, IsDriver
from api import error_messages
from .schemas import (
    driver_schemas,
    general_schemas,
    passenger_schemas,
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
    user = (
        User.objects.select_related('residence_city', 'type')
        .only(
            'id_user',
            'email',
            'identity_document',
            'phone_number',
            'first_name',
            'last_name',
            'date_of_birth',
            'residence_city',
            'type',
            'is_active',
        )
        .get(id_user=user.id_user)
    )
    serializer = ViewUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Mostrar datos en la página de inicio
@extend_schema(**general_schemas.home_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    user = request.user
    content = {'name': user.first_name}
    return Response(content, status=status.HTTP_200_OK)


# Conductores


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

    vehicle = VehicleSerializerForDriver(data=vehicle_data)

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

        serializer = VehicleSerializerForDriver(
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
def get_trip_driver(request, id_trip):
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
                'pickup_point',
                'seats',
                'is_confirmed',
                'passenger__phone_number',
                'passenger__first_name',
                'passenger__last_name',
            )
        )
        serializer = ViewPassenger_TripSerializerForDriver(queryset, many=True)
        content = {'id_trip': id_trip, 'passengers': serializer.data}
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': error_messages.TRIP_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener historial de viajes
# @extend_schema(**driver_schemas.my_vehicles_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trip_history_driver(request):
    user = request.user
    current_datetime = timezone.now()

    queryset = Trip.objects.only(
        'id_trip', 'start_date', 'start_time', 'starting_point', 'arrival_point'
    ).annotate(
        start_datetime=ExpressionWrapper(
            F('start_date') + F('start_time'), output_field=DateTimeField()
        )
    )

    queryset = queryset.filter(
        start_datetime__lt=current_datetime, driver=user.id_user
    ).order_by(
        '-start_datetime'
    )  # lt signifia less than.

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    serializer = ViewTripReduceSerializer(paginated_results, many=True)
    return paginator.get_paginated_response(serializer.data)


# Obtener viajes planeados
# @extend_schema(**driver_schemas.my_vehicles_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def planned_trips_driver(request):
    user = request.user
    current_datetime = timezone.now()

    queryset = Trip.objects.only(
        'id_trip', 'start_date', 'start_time', 'starting_point', 'arrival_point'
    ).annotate(
        start_datetime=ExpressionWrapper(
            F('start_date') + F('start_time'), output_field=DateTimeField()
        )
    )

    queryset = queryset.filter(
        start_datetime__gt=current_datetime, driver=user.id_user
    ).order_by(
        'start_datetime'
    )  # gt signifia greater than.

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    serializer = ViewTripReduceSerializer(paginated_results, many=True)
    return paginator.get_paginated_response(serializer.data)


# Obtener viaje actual
# @extend_schema(**driver_schemas.my_vehicles_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_trip(request):
    user = request.user
    current_datetime = timezone.now()
    two_hours_ago = timezone.now() - timedelta(hours=2)

    queryset = Trip.objects.only(
        'id_trip', 'start_date', 'start_time', 'starting_point', 'arrival_point'
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
    )  # lte signifia less than equal.

    serializer = ViewTripReduceSerializer(queryset)
    return Response(serializer.data, status=status.HTTP_200_OK)


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

        '''Si el método es PUT debe tener todos los campos.'''
        partial = False if request.method == 'PUT' else True

        serializer = TripSerializer(trip, data=trip_data, partial=partial)

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


# Obtener viaje asociado
@extend_schema(**passenger_schemas.get_trip_passenger_associated)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trip_passenger_associated(request, id_trip):
    user = request.user
    try:
        passenger_Trip = Passenger_Trip.objects.only(
            'pickup_point',
            'seats',
            'is_confirmed',
        ).get(trip=id_trip, passenger=user.id_user)
        passenger_trip_serializer = ViewPassenger_TripSerializerForPassenger(
            passenger_Trip
        )

        trip = (
            Trip.objects.select_related(
                'driver',
            )
            .only(
                'start_date',
                'start_time',
                'starting_point',
                'arrival_point',
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
        vehicle_serializer = ViewVehicleSerializerForPassenger(vehicle)

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
# @extend_schema(**passenger_schemas.get_trip_passenger_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trip_passenger(request, id_trip):
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

        trip_serializer = ViewTripDriverSerializer(trip)
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
        vehicle_serializer = ViewVehicleSerializerForPassenger(vehicle)

        content = trip_data
        content['vehicle'] = vehicle_serializer.data
        return Response(content, status=status.HTTP_200_OK)

    except Trip.DoesNotExist:
        return Response(
            {'error': error_messages.TRIP_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )


# Obtener historial de viajes
# @extend_schema(**driver_schemas.my_vehicles_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trip_history_passenger(request):
    user = request.user
    current_datetime = timezone.now()

    queryset = (
        Passenger_Trip.objects.select_related('trip')
        .only(
            'trip',
            'trip__start_date',
            'trip__start_time',
            'trip__starting_point',
            'trip__arrival_point',
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
    content = [serialize_passenger_trip(item) for item in paginated_results]
    return paginator.get_paginated_response(content)


# Obtener viajes planeados
# @extend_schema(**driver_schemas.my_vehicles_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def planned_trips_passenger(request):
    user = request.user
    current_datetime = timezone.now()

    queryset = (
        Passenger_Trip.objects.select_related('trip')
        .only(
            'trip',
            'trip__start_date',
            'trip__start_time',
            'trip__starting_point',
            'trip__arrival_point',
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
    content = [serialize_passenger_trip(item) for item in paginated_results]
    return paginator.get_paginated_response(content)
