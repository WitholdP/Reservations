from datetime import date, datetime

from django.conf import settings
from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return self.room_name


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    comment = models.TextField()

    def datecheck(self):
        """Checks if the date put in the for is not fromt he past"""
        return self.reservation_date < datetime.today().date()

    class Meta:
        unique_together = ("room", "reservation_date")
