from django.urls import path

from . import views

urlpatterns = [
    path("applications/", views.ListCreateApplicationView.as_view())
]