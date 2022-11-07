from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status

from .models import User
from .permissions import IsAdminOrReadOnly, IsAuthenticated, IsOwnerOrAdmin
from .serializers import LoginSerializer, UserSerializer


<<<<<<< HEAD
class LoginView(APIView):
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

        return Response(
            {"detail": "invalid email or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    ...
=======
class UserView(generics.CreateAPIView):
    serializer_class = UserSerializer
>>>>>>> development


class UserView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    ...


class UserDetailView(generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    serializer_class = UserSerializer
<<<<<<< HEAD
    lookup_url_kwarg = "user_id"
=======
    lookup_url_kwarg = 'user_id'
>>>>>>> development
    queryset = User.objects.filter()
