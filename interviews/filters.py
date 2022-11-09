from django_filters import rest_framework as filters

from .models import Interview


class InterviewFilter(filters.FilterSet):
    class Meta:
        model = Interview
        fields = {
            "schedule": ["exact", "lt", "gt"],
        }
