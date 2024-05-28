from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Solo permite el acceso de usuarios de tipo Admin.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_staff and request.user.type.name == 'Admin')


class IsDriver(BasePermission):
    """
    Solo permite el acceso de usuarios de tipo Conductor.
    """

    def has_permission(self, request, view):
        return bool(request.user.type.name == 'Conductor')


class IsPassenger(BasePermission):
    """
    Solo permite el acceso de usuarios de tipo Pasajero.
    """

    def has_permission(self, request, view):
        return bool(request.user.type.name == 'Pasajero')
