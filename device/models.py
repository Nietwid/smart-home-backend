from django.db.models import JSONField
from django.db import models

from room.models import Room
from user.models import Home


class Router(models.Model):
    ip = models.CharField(max_length=100, default="")
    mac = models.CharField(max_length=100)
    home = models.OneToOneField(Home, on_delete=models.CASCADE, related_name="router")
    wifi_strength = models.IntegerField(default=0)
    last_seen = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.mac


class ChipType(models.TextChoices):
    ESP32 = "ESP32", "esp32"
    ESP8266 = "ESP8266", "esp8266"
    ESP8266_01 = "ESP8266_01", "esp8266_01"


class Device(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, related_name="devices", null=True, default=None
    )
    home = models.ForeignKey(
        Home, on_delete=models.CASCADE, related_name="devices", null=True
    )
    name = models.CharField(max_length=100, default="Unknown")
    last_seen = models.DateTimeField(auto_now_add=True, auto_created=True)
    mac = models.CharField(max_length=100)
    wifi_strength = models.IntegerField(default=0)
    pending = JSONField(default=list, blank=True)
    is_online = models.BooleanField(default=False)
    firmware_version = models.FloatField(default=1.0)
    chip_type = models.CharField(
        max_length=100, choices=ChipType, default=ChipType.ESP32
    )
    svg_id = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_router(self):
        return Router.objects.get(home=self.home)

    def get_router_mac(self):
        return Router.objects.filter(home=self.home).only("mac").first()

    def extra_settings(self):
        return {}

    def make_intent(self, data: dict) -> None:
        return


class Event(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="events")
    target_device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    action = models.CharField(max_length=100, null=True)
    event = models.CharField(max_length=100, null=True)
    extra_settings = models.JSONField(default=dict)
