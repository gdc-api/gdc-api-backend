import ipdb
from applications.models import Application
from applications.serializers import ApplicationSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):

    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = Interview
        exclude = ["user"]
        read_only_fields = ["id"]

    ...


class InterviewToggleSerializer(serializers.ModelSerializer):

    was_approved = serializers.SerializerMethodField(read_only=True)

    def get_was_approved(self, obj: Interview):
        return obj.toggle_was_approved()

    class meta:
        model = Interview
        fields = "__all__"
        read_only_fields = [
            "id",
            "application",
            "schedule",
            "locations",
        ]

    ...
