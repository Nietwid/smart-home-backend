from django.db import models
from device.models import Device
from peripherals.models import Peripherals


# Create your models here.
class Rule(models.Model):

    name = models.CharField(max_length=200)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    is_local = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class RuleTrigger(models.Model):

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name="triggers")
    peripheral = models.ForeignKey(Peripherals, on_delete=models.CASCADE)
    event = models.CharField(max_length=50)
    extra_settings = models.JSONField(default=dict)


class RuleCondition(models.Model):

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name="conditions")
    peripheral = models.ForeignKey(
        Peripherals, on_delete=models.CASCADE, null=True, blank=True
    )
    operator = models.CharField(max_length=20)
    value = models.CharField(max_length=100)


class RuleAction(models.Model):

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name="actions")
    peripheral = models.ForeignKey(Peripherals, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    extra_settings = models.JSONField(default=dict)
    order = models.IntegerField(default=0)
