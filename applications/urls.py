from django.urls import path

from . import views

urlpatterns = [
    path("applications/", views.ListCreateApplicationView.as_view()),
    path(
        "applications/company/<str:pk>/",
        views.CreateApplicationWithCompanyIdView.as_view()
    ),
    path("applications/<str:pk>/", views.ApplicationDetailView.as_view())
]