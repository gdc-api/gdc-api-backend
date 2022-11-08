from django_filters import rest_framework as filters

from .models import Application

class ApplicationFilter(filters.FilterSet):
    job__title_icontains = filters.CharFilter(
        field_name="job__title", lookup_expr="icontains",
    )
    job__url_icontains = filters.CharFilter(
        field_name="job__url", lookup_expr="icontains"
    )
    job__level_icontains = filters.CharFilter(
        field_name="job__level", lookup_expr="icontains"
    )
    job__category_icontains = filters.CharFilter(
        field_name="job__category", lookup_expr="icontains"
    )
    job__period_icontains = filters.CharFilter(
        field_name="job__period", lookup_expr="icontains"
    )
    job__estimated_pay_lte = filters.NumberFilter(
        field_name="job__estimated_pay", lookup_expr="lte"
    )
    job__estimated_pay_gte = filters.NumberFilter(
        field_name="job__estimated_pay", lookup_expr="gte"
    )
    job__location_icontains = filters.CharFilter(
        field_name="job__locations", lookup_expr="icontains"
    )
    job__contract_icontains = filters.CharFilter(
        field_name="job__contract", lookup_expr="icontains"
    )


    job__company__name = filters.CharFilter(
        field_name="job__company__name", lookup_expr="icontains"
    )
    job__company__description = filters.CharFilter(
        field_name="job__comapny__description", lookup_expr="icontains"
    )
    job__company__segment = filters.CharFilter(
        field_name="job__company__segment", lookup_expr="icontains"
    )

    class Meta:
        model = Application
        fields = [
            "job__url",
            "job__title",
            "job__level",
            "job__category",
            "job__period",
            "job__estimated_pay",
            "job__location",
            "job__contract",

            "job__company__id",
            "job__company__name",
            "job__company__description",
            "job__company__segment"
        ]
