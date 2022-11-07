from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        
        exclude = [
          'is_superuser',
          'last_login',
          'groups',
          'date_joined',
          'is_active',
          'user_permissions',
          "is_staff"
        ]

        read_only_fields = ['id']
        extra_kwargs = {
          'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  
