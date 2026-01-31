from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


def get_unique_uuid():
    return uuid4().hex


class Home(models.Model):
    users = models.ManyToManyField(User, related_name="home")
    add_uid = models.UUIDField(default=get_unique_uuid)


class Favourite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    device = models.ManyToManyField("device.Device")
    room = models.ManyToManyField("room.Room")
    camera = models.ManyToManyField("camera.Camera")

    def __str__(self):
        return self.user.username
