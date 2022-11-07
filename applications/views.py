from django.shortcuts import render
from rest_framework import generics

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .models import Application
from .serializers import ApplicationSerializer, ApplicationSerializerCreation, ApplicationSerializerCreationWithoutCompanySerializer

import ipdb

# Create your views here.
class ListCreateApplicationView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated or IsAdminUser]

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializerCreation

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
        


