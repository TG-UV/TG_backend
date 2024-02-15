from rest_framework import status, generics, permissions, authentication
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import UserCustomSerializer, CitySerializer
from .models import User, City


# Admins


# Listar todos los usuarios
class ListUsersView(generics.ListAPIView):
    serializer_class = UserCustomSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


'''
# Crear usuario admin con todos los permisos
class CreateSuperuserView(generics.CreateAPIView):
    serializer_class = UserCustomSerializer


class UpdateSuperuserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserCustomSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
'''


# Vistas de registro


# Obtener datos para el registro
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def registration(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    content = serializer.data
    return Response(content, status=status.HTTP_200_OK)


# Conductores


# Mostrar datos en la página de inicio
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def home_driver(request):

    id_user = request.user.id_user
    try:
        # Busca el conductor según el id del usuario que ha iniciado sesión
        driver = User.objects.get(id_user=id_user, type__name='Conductor')
        serializer = UserCustomSerializer(driver)
        content = {'name': serializer.data['first_name']}
        return Response(content, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(
            {'error': 'No existe conductor con ese id'},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Pasajeros


# Mostrar datos en la página de inicio
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def home_passenger(request):

    id_user = request.user.id_user
    try:
        # Busca el pasajero según el id del usuario que ha iniciado sesión
        passenger = User.objects.get(id_user=id_user, type__name='Pasajero')
        serializer = UserCustomSerializer(passenger)
        content = {'name': serializer.data['first_name']}
        return Response(content, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(
            {'error': 'No existe pasajero con ese id'},
            status=status.HTTP_400_BAD_REQUEST,
        )


'''@api_view(["POST"])
def signin(request):
    email = request.POST['email']
    password = request.POST['password']

    if email and password:
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {'error': 'correo o contraseña incorrecta'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            login(request, user)
            return Response(
                {'mensaje': 'Sesión iniciada'}, status=status.HTTP_200_OK
            )

    else:
        return Response(
            {'error': 'los campos de correo y contraseña son requeridos'},
            status=status.HTTP_400_BAD_REQUEST,
        )
'''
