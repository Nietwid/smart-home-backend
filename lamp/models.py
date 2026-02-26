import datetime
from django.db import models

from device.models import Device
from enum import Enum


def default_time():
    return datetime.datetime.now().replace(second=0, microsecond=0).time()


class Lamp(Device):
    led_start = models.TimeField(default=default_time)
    light_start = models.TimeField(default=default_time)
    light_stop = models.TimeField(default=default_time)
    brightness = models.SmallIntegerField(default=100)
    step = models.SmallIntegerField(default=21)
    lighting_time = models.SmallIntegerField(default=10)

    def available_actions(self):
        return [
            # MessageEvent.ON.value,
            # MessageEvent.OFF.value,
            # MessageEvent.TOGGLE.value,
            # MessageEvent.BLINK.value,
        ]

    def extra_settings(self):
        return {"reverse": "bool"}
