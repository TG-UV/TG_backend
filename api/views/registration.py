from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from api.schemas import registration_schemas
from api.models import (
    City,
    VehicleColor,
    VehicleBrand,
    VehicleType,
    VehicleModel,
)


# Obtener datos para el registro
@extend_schema(**registration_schemas.registration_schema)
@api_view(['GET'])
@permission_classes([AllowAny])
def registration(request):
    content = City.objects.all().values()
    return Response(content, status=status.HTTP_200_OK)


# Obtener datos para registrar un vehículo
@extend_schema(**registration_schemas.vehicle_registration_schema)
@api_view(['GET'])
@permission_classes([AllowAny])
def vehicle_registration(request):
    colors = VehicleColor.objects.all().values()
    brands = VehicleBrand.objects.all().values()
    types = VehicleType.objects.all().values()
    models = VehicleModel.objects.all().values()

    content = {
        'types': types,
        'brands': brands,
        'models': models,
        'colors': colors,
    }
    return Response(content, status=status.HTTP_200_OK)
