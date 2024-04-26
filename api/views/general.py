from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from api.serializers.user import ViewUserSerializer
from api.models import User
from api.schemas import general_schemas
from djoser.views import UserViewSet


# Todos los usuarios
class CustomUserViewSet(UserViewSet):
    @action(['get', 'patch'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action([], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        return

    @action([], detail=False, url_path=f"reset_{User.USERNAME_FIELD}")
    def reset_username(self, request, *args, **kwargs):
        return

    @action([], detail=False, url_path=f"reset_{User.USERNAME_FIELD}_confirm")
    def reset_username_confirm(self, request, *args, **kwargs):
        return


# Ver perfil
@extend_schema(**general_schemas.get_profile_schema)
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