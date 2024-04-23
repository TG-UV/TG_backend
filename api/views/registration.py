from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from api.serializers.city import CitySerializer
from api.models import City
from api.schemas import registration_schemas
from api.serializers.vehicle_color import VehicleColorSerializer
from api.serializers.vehicle_brand import VehicleBrandSerializer
from api.serializers.vehicle_type import VehicleTypeSerializer
from api.serializers.vehicle_model import VehicleModelSerializer
from api.models import (
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
    queryset = City.objects.all()
    serializer = CitySerializer(queryset, many=True)
    content = serializer.data
    return Response(content, status=status.HTTP_200_OK)


# Obtener datos para registrar un vehículo
@extend_schema(**registration_schemas.vehicle_registration_schema)
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
