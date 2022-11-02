from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # job = JobSerializer()

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["created_at"]