from rest_framework import permissions
from rest_framework.views import Request, View


class IsAdminOrPost(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return bool(request.method == "POST" or request.user and request.user.is_staff)
