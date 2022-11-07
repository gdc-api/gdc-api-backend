from companies.serializers import CompanySerializer
from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):

    company = CompanySerializer()

    class Meta:
        model = Job
        fields = "__all__"

    ...
