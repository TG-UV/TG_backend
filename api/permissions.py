from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_staff and request.user.type.name == 'Admin'
        )


class IsDriver(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.type.name == 'Conductor')


class IsPassenger(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.type.name == 'Pasajero')
