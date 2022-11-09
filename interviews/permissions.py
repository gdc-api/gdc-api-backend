from rest_framework import permissions
from rest_framework.views import Request, View


class IsAdminPostOrGet(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return bool(
            request.method == "GET"
            or request.method == "POST"
            or request.user
            and request.user.is_staff
        )
