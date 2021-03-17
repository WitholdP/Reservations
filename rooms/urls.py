from django.urls import path

from rooms.views import AddRoom, Index, RoomDelete, Rooms

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("rooms/", Rooms.as_view(), name="rooms"),
    path("add_room/", AddRoom.as_view(), name="add_room"),
    path("room_delete/<int:room_id>/", RoomDelete.as_view(), name="room_delete"),
]
