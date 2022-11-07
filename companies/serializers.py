from rest_framework import serializers
from companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        mode = Company
        fields = "__all__"
        read_only_fields = ["id"]
