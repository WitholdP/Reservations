from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()
    projector = models.BooleanField(default=False)
