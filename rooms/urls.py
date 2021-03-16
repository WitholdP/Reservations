from django.urls import path

from rooms.views import AddRoom, Index, Rooms

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("rooms/", Rooms.as_view(), name="rooms"),
    path("add_room/", AddRoom.as_view(), name="add_room"),
]
