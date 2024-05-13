from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from django.db import IntegrityError, transaction
from drf_spectacular.utils import extend_schema
from api.serializers.user import ViewUserSerializer
from api.serializers.device import DeviceSerializer
from api.models import User, Device
from api.schemas import general_schemas
from djoser.views import UserViewSet, TokenCreateView, TokenDestroyView


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


# Iniciar sesión
class CustomLogin(TokenCreateView):

    def __init__(self):
        self.id_device = None

    def post(self, request, **kwargs):
        self.id_device = request.data.get('id_device', None)

        return super().post(request, **kwargs)

    def _action(self, serializer):
        login_response = super()._action(serializer)
        auth_token = login_response.data.get('auth_token', None)

        if auth_token and self.id_device:
            self.add_device(auth_token)

        return login_response

    def add_device(self, auth_token):
        try:
            token = Token.objects.only('user_id').get(key=auth_token)
            device_data = {'id_device': self.id_device, 'user': token.user_id}

            device = DeviceSerializer(data=device_data)

            if device.is_valid():
                device.save()

        except Token.DoesNotExist:
            return

        except IntegrityError:
            return


# Cerrar sesión
class CustomLogout(TokenDestroyView):
    def post(self, request):
        user = request.user
        with transaction.atomic():
            Device.objects.filter(user=user.id_user).delete()
            return super().post(request)


# Ver perfil
@extend_schema(**general_schemas.get_profile_schema)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    user = User.objects.get_user_profile(user.id_user)
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
