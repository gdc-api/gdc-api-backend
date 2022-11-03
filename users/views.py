from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import User
from .permissions import IsAdmin, IsAuthenticated, IsOwner


class UserView(generics.CreateAPIView):
    # serializer_class = UserSerializer
    ...


class AdminListAllUsersView(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    # serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    # serializer_class = PatchUserSerializer
    lookup_url_kwarg = 'user_id'
    queryset = User.objects.filter()

