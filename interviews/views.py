from datetime import datetime

import ipdb
from applications.models import Application
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .filters import InterviewFilter
from .models import Interview
from .permissions import IsAdminPostOrGet
from .serializers import InterviewSerializer, InterviewToggleSerializer


class InterviewView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminPostOrGet]

    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    filterset_class = InterviewFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset

        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    ...

    def perform_create(self, serializer):
        passed = False

        now = datetime.now()
        schedule = self.request.data["schedule"]
        datetime_schedule = datetime.fromisoformat(schedule)

        if datetime_schedule < now:
            passed = True

        application_id = self.request.data.pop("application")
        application = Application.objects.get(pk=application_id)

        serializer.save(application=application, user=self.request.user, passed=passed)

    ...


class InterviewDetailView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "interview_id"
    queryset = Interview.objects.filter()
    serializer_class = InterviewSerializer

    ...


class InterviewToggleView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "interview_id"
    queryset = Interview.objects.filter()
    serializer_class = InterviewToggleSerializer

    ...
