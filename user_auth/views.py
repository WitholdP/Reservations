from django.shortcuts import render
from django.views import View


class LogIn(View):
    template = "user_auth/login.html"

    def get(self, request):
        return render(request, self.template)
