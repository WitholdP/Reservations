from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("rooms.urls")),
    path("accounts/", include("user_auth.urls")),
]
