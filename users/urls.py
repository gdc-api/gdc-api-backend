from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import AdminListAllUsersView, UserDetailView, UserView

urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/', AdminListAllUsersView.as_view()),
    path('users/<str:user_id>/', UserDetailView.as_view()),
    path("login/", obtain_auth_token)

]
