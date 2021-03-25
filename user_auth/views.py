from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, reverse
from django.views import View

from .forms import LogInForm


class LogIn(View):
    template = "user_auth/login.html"
    form = LogInForm()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        message_danger = request.GET.get("message_danger", None)
        return render(
            request,
            self.template,
            {"form": self.form, "message_danger": message_danger},
        )

    def post(self, request):
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                print(user.first_name)
                message_success = f"Login succesfull {user.first_name}"
                return redirect(
                    reverse("index") + f"?message_success={message_success}"
                )
            message_danger = "Wrong email or password"
            return redirect(reverse("log_in") + f"?message_danger={message_danger}")


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        message_success = f"Logout succesfull"
        return redirect(reverse("index") + f"?message_success={message_success}")
    else:
        return redirect("/")
