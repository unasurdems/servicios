from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import CurrentUserAPIView, GetMenuAPIView


urlpatterns = [
    path('api/get_token/', obtain_auth_token, name='obtain_auth_token'),
    path('api/me/', CurrentUserAPIView.as_view(), name='current_user'),
    path('api/get_menu/', GetMenuAPIView.as_view(), name='get_menu'),
]