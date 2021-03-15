from django.urls import path

from rooms.views import Index

urlpatterns = [
    path("", Index.as_view(), name="index"),
]
