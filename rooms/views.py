from django.shortcuts import render
from django.views import View


class Index(View):
    """Home view Displaying all the rooms"""

    def get(self, request):
        return render(request, "rooms/index.html")
