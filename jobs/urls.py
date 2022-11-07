from django.urls import path
from .views import JobDetailView

urlpatterns = [
    path("jobs/<str:job_id>/", JobDetailView.as_view()),
]
