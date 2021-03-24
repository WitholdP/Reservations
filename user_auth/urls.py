from django.urls import path

from user_auth.views import LogIn

urlpatterns = [
    path("login/", LogIn.as_view(), name="log_in"),
]
