from rest_framework.permissions import BasePermission
from users.models import User
from .models import Application


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, application):
        user_applications = request.user.applications
    
        try:
            user_applications.get(id=application.id)
        except Application.DoesNotExist:
            return False
        
        return True
