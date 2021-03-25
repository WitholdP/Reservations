from django.urls import path

from .views import LogIn, log_out

urlpatterns = [
    path("login/", LogIn.as_view(), name="log_in"),
    path("logout/", log_out, name="log_out"),
]
