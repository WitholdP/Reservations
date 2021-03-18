from django.urls import path

from rooms.views import Index, RoomAdd, RoomDelete, RoomEdit, RoomReservation, Rooms

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("rooms/", Rooms.as_view(), name="rooms"),
    path("room_add/", RoomAdd.as_view(), name="room_add"),
    path("room_delete/<int:room_id>/", RoomDelete.as_view(), name="room_delete"),
    path("room_edit/<int:room_id>", RoomEdit.as_view(), name="room_edit"),
    path("room_reserve/<int:room_id>", RoomReservation.as_view(), name="room_reserve"),
]
