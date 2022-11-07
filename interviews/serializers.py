from rest_framework import serializers
from .models import Interview

from applications.serializers import ApplicationSerializer
from applications.models import Application


class InterviewSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = Interview
        fields = "__all__"
        read_only_fields = ["id"]

    def create(self, validated_data):
        application_id = validated_data.pop("application")
        application = Application.objects.get(application_id)

        validated_data["application"] = application

        return super().create(validated_data)

    ...
