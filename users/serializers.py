from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    ...


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
<<<<<<< HEAD

        exclude = [
            "username",
            "is_superuser",
            "last_login",
            "groups",
            "user_permissions",
=======
        
        exclude = [
          'is_superuser',
          'last_login',
          'groups',
          'date_joined',
          'is_active',
          'user_permissions',
          "is_staff"
>>>>>>> development
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
