from django.db import models
from device.models import Device


class Peripherals(models.Model):
    device = models.ForeignKey(
        Device, related_name="peripherals", on_delete=models.CASCADE
    )
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    config = models.JSONField(default=dict, blank=True)
    state = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.name} on {self.device.name}"


class RfidCard(models.Model):
    uid = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(auto_now=True)
    allowed_peripherals = models.ManyToManyField("peripherals.Peripherals", blank=True)
