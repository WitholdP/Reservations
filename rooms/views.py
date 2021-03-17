from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from rooms.models import Room


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
