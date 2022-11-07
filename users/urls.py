from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserDetailView, UserView, LoginView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/", UserView.as_view()),
    path("users/<str:user_id>/", UserDetailView.as_view()),
    path("login/", LoginView.as_view()),
]
