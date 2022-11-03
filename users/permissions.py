from rest_framework import permissions
from rest_framework.views import Request, View

from users.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_superuser


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User) -> bool:
        return user.id == request.user.id
