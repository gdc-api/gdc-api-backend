from django.urls import path

from . import views

urlpatterns = [
    path("interviews/", views.InterviewView.as_view()),
    path("interviews/<str:interview_id>/", views.InterviewDetailView.as_view()),
    path("interviews/<str:interview_id>/toggle/", views.InterviewToggleView.as_view()),
]
