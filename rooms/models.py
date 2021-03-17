from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return self.room_name


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    date = models.DateField()
    comment = models.TextField()

    class Meta:
        unique_together = ('room', 'date')
