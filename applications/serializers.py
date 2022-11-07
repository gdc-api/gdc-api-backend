from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import Application

from users.serializers import UserSerializer
from jobs.serializers import JobSerializer, JobWithoutCompanySerializer

from companies.models import Company
from jobs.models import Job

import ipdb

class ApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    job = JobSerializer()

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["created_at", "id"]


class ApplicationSerializerCreation(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job = JobSerializer()

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["created_at", "id"]

    
    def create(self, validated_data):
        company_data = validated_data["job"].pop("company")
        company = Company.objects.create(**company_data)
        
        job_data = validated_data.pop("job")
        job_data["company"] = company
        job = Job.objects.create(**job_data)
        
        application_data = {
            "user":validated_data["user"],
            "job":job
        }

        application = Application.objects.create(**application_data)
        return application

class ApplicationSerializerCreationWithoutCompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job = JobWithoutCompanySerializer()

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["created_at", "id"]
    
    def create(self, validated_data):
        company_id = validated_data.pop("company_id")
        user = validated_data["user"]
        try:
            company = Company.objects.filter(jobs__applications__user__id=user.id)
            company = company.filter(id=company_id).first()
        except Company.DoesNotExist:
            raise NotFound("Company not found")
        
        if not company:
            raise NotFound("Company not found")
        
        job_data = validated_data["job"]
        job = Job.objects.create(**job_data, company=company)


        application_data = {
            "user":user,
            "job":job
        }

        application = Application.objects.create(**application_data)
        return application