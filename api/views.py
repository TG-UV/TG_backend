from rest_framework import status, generics, permissions, authentication
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SuperuserSerializer
from .models import User


# Vistas para admins
# Listar todos los usuarios
class ListUsersView(generics.ListAPIView):
    serializer_class = SuperuserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

class CreateSuperuserView(generics.CreateAPIView):
    serializer_class = SuperuserSerializer

class UpdateSuperuserView(generics.RetrieveUpdateAPIView):
    serializer_class = SuperuserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
'''
class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer'''


# Vistas para pasajeros
# Mostrar datos en la página de inicio
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home_passenger(request):
    content = {'name': request.user.first_name}
    return Response(content)


'''@api_view(["POST"])
def signin(request):
    email = request.POST['email']
    password = request.POST['password']

    if email and password:
        user = authenticate(request, email=email, password=password)

        if user is None:
            return JsonResponse(
                {'error': 'correo o contraseña incorrecta'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            login(request, user)
            return JsonResponse(
                {'mensaje': 'Sesión iniciada'}, status=status.HTTP_200_OK
            )

    else:
        return JsonResponse(
            {'error': 'los campos de correo y contraseña son requeridos'},
            status=status.HTTP_400_BAD_REQUEST,
        )
'''
