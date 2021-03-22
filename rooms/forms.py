from django import forms
from django.forms import ModelForm

from .models import Reservation, Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ["room_name", "capacity", "projector"]
        widgets = {
            "room_name": forms.TextInput(attrs={"class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "projector": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
