from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .models import Job
from .serializers import JobWithoutCompanySerializer


class JobDetailView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = JobWithoutCompanySerializer
    lookup_url_kwarg = "job_id"
    queryset = Job.objects.filter()
    ...
