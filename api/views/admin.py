from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from api.serializers.user import ExtendedUserSerializer
from api.models import User
from api.permissions import IsAdmin
from api.schemas import admin_schemas


# Listar todos los usuarios
@extend_schema(**admin_schemas.list_users_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def list_users(request):
    queryset = User.objects.all().order_by('id_user')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_results = paginator.paginate_queryset(queryset, request)
    serializer = ExtendedUserSerializer(paginated_results, many=True)
    return paginator.get_paginated_response(serializer.data)
