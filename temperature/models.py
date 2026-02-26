from django.db import models

from device.models import Device
from django.utils import timezone


class TempHum(Device):
    temperature = models.FloatField(default=None, blank=True, null=True)
    humidity = models.FloatField(default=None, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    temperature_hysteresis = models.FloatField(default=1.5)
    humidity_hysteresis = models.FloatField(default=5)
    trigger_temp_up = models.FloatField(default=25)
    trigger_temp_down = models.FloatField(default=15)
    trigger_hum_up = models.FloatField(default=70)
    trigger_hum_down = models.FloatField(default=30)

    def available_events(self):
        return [
            # MessageEvent.ON_MEASUREMENT_TEMP_HUM.value,
            # MessageEvent.ON_TEMPERATURE_ABOVE.value,
            # MessageEvent.ON_TEMPERATURE_BELOW.value,
            # MessageEvent.ON_HUMIDITY_ABOVE.value,
            # MessageEvent.ON_HUMIDITY_BELOW.value,
        ]
