from rest_framework import generics

# exceptions
from rest_framework.exceptions import NotAcceptable

# filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApplicationFilter

# authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwner

# models and serializers
from .models import Application
from .serializers import ApplicationSerializer, ApplicationSerializerCreation, ApplicationSerializerCreationWithoutCompanySerializer


class ListCreateApplicationView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated or IsAdminUser]

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializerCreation

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ApplicationFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset

        queryset = self.queryset.filter(user__id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateApplicationWithCompanyIdView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializerCreationWithoutCompanySerializer

    def perform_create(self, serializer):
        company_id = self.kwargs["pk"]
        serializer.save(company_id=company_id, user=self.request.user)


class ApplicationDetailView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated and IsOwner]

    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()

    def perform_destroy(self, instance):
        if not instance.is_active:
            raise NotAcceptable("Application is already innactive")

        instance.is_active = False
        instance.save()
