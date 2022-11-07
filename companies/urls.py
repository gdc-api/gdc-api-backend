from django.urls import path

from . import views

urlpatterns = [
    path("companies/<pk>/", views.CompanyDetailView.as_view())
]