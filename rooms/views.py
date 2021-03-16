from django.shortcuts import redirect, render
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


class AddRoom(View):
    """ Displays form for adding a new room to the database. """

    def get(self, request):
        return render(request, "rooms/add_room.html")

    def post(self, request):
        room_name = request.POST.get("room_name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector")
        if projector:
            projector = True
        else:
            projector = False
        new_room = Room(room_name=room_name, capacity=capacity, projector=projector)
        new_room.save()
        return redirect(f"/rooms/?message_success=Room {room_name} succesfully added")
