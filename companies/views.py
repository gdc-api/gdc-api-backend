from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from companies.models import Company
from companies.serializers import CompanySerializer


class CompanyDetailView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
