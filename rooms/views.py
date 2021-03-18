from datetime import datetime

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from rooms.models import Reservation, Room


class Index(View):
    """ Home page """

    def get(self, request):

        return render(request, "rooms/index.html")


class Rooms(View):
    """ Displays all the rooms in form of the table """

    def get(self, request):
        message_success = request.GET.get("message_success", None)
        message_danger = request.GET.get("message_danger", None)
        rooms = Room.objects.all().order_by("pk")
        for room in rooms:
            reservation_dates = [res.reservation_date for res in room.reservation_set.all()]
            room.reserved = datetime.now().date() in reservation_dates
        # search for a specific room name
        search = request.GET.get("room_name")
        if search:
            rooms = rooms.filter(room_name__icontains=search)
        context = {
            "message_success": message_success,
            "message_danger": message_danger,
            "rooms": rooms,
        }
        return render(request, "rooms/rooms.html", context)


class RoomAdd(View):
    """ Displays form for adding a new room to the database. """

    def get(self, request):
        message_danger = request.GET.get("message_danger", None)
        return render(
            request, "rooms/room_add.html", {"message_danger": message_danger}
        )

    def post(self, request):
        room_name = request.POST.get("room_name")
        if not room_name:  # check if roomname is not empty
            return redirect(
                reverse("add_room") + f"?message_danger=Room name can't be empty"
            )

        capacity = int(request.POST.get("capacity"))
        if capacity < 1:  # checking if capacity is more than 0
            return redirect(
                reverse("add_room") + f"?message_danger=Capacity has to be more than 0"
            )

        projector = request.POST.get("projector")
        if projector:
            projector = True
        else:
            projector = False

        new_room = Room(room_name=room_name, capacity=capacity, projector=projector)
        try:
            new_room.save()
        except:
            return redirect(
                reverse("add_room")
                + f"?message_danger=Room with name {room_name} already exists"
            )

        return redirect(
            reverse("rooms") + f"?message_success=Room {room_name} has been created"
        )


class RoomDelete(View):
    """Renders the template for the room deletion. It will contain the form
    where user has to confirm the actual deletion fo the room from the database
    - simply by typing in DELETE"""

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        message_danger = request.GET.get("message_danger", None)
        context = {
            "room": room,
            "message_danger": message_danger,
        }
        return render(request, "rooms/room_delete.html", context)

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        confirmation = request.POST.get("delete")
        if confirmation != "DELETE":
            return redirect(
                reverse("room_delete", args=[room.id])
                + "?message_danger=You have to type DELETE to confirm"
            )
        message = f"Room {room.room_name} was succesfully deleted"
        room.delete()
        return redirect(reverse("rooms") + f"?message_success={message} ")


class RoomEdit(View):
    """View for editing the specific room. It will aply same form validation as
    RoomAdd view."""

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        message_success = request.GET.get("message_success", None)
        message_danger = request.GET.get("message_danger", None)
        context = {
            "room": room,
            "message_success": message_success,
            "message_danger": message_danger,
        }
        return render(request, "rooms/room_edit.html", context)

    def post(self, request, room_id):
        room_name = request.POST.get("room_name")
        if not room_name:
            return redirect(
                reverse("room_edit", args=[room_id])
                + "?message_danger=Room name can't be empty"
            )

        capacity = int(request.POST.get("capacity"))
        if capacity < 1:
            return redirect(
                reverse("room_edit", args=[room_id])
                + "?message_danger=Capacity has to be more than 0"
            )

        projector = request.POST.get("projector")
        if projector:
            projector = True
        else:
            projector = False

        room = Room.objects.get(pk=room_id)
        room.room_name = room_name
        room.capacity = capacity
        room.projector = projector
        try:
            room.save()
        except:
            return redirect(
                reverse("room_edit", args=[room_id])
                + f"?message_danger=Room with name {room_name} already exists"
            )

        return redirect(
            reverse("room_edit", args=[room_id])
            + "?message_success=Room succesfully edited"
        )


class RoomReservation(View):
    """View for adding a reservation for a specific room"""

    def get(self, request, room_id):
        message_success = request.GET.get("message_success", None)
        message_danger = request.GET.get("message_danger", None)
        room = Room.objects.get(pk=room_id)
        context = {
            "room": room,
            "message_success": message_success,
            "message_danger": message_danger,
        }
        return render(request, "rooms/room_reserve.html", context)

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        # time below is converted from strin to date, and later to django format YYYY-MM-DD
        reservation_date = datetime.strptime(
            request.POST.get("reservation_date"), "%m/%d/%Y"
        ).date()
        comment = request.POST.get("comment")
        new_reservation = Reservation(
            room=room, reservation_date=reservation_date, comment=comment
        )
        if new_reservation.datecheck():
            return redirect(
                reverse("room_reserve", args=[room_id])
                + f"?message_danger=Date can't be in the past"
            )

        if Reservation.objects.filter(room=room, reservation_date=reservation_date):
            return redirect(
                reverse("room_reserve", args=[room_id])
                + f"?message_danger=There is already reservation that day"
            )

        new_reservation.save()
        return redirect(
            reverse("room_reserve", args=[room_id])
            + f"?message_success=Succesfully reserved room {room} for the {reservation_date}"
        )


def reservation_delete(request, reservation_id, room_id):
    """Function for deleting specific reservation"""
    reservation = Reservation.objects.get(pk=reservation_id)
    message = f"reservation {reservation.reservation_date} was succesfully deleted"
    reservation.delete()

    return redirect(
        reverse("room_reserve", args=[room_id]) + f"?message_success={message}"
    )
