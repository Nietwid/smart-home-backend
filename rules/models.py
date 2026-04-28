from django.db import models


class Rule(models.Model):

    name = models.CharField(max_length=200, blank=True, null=True)
    device = models.ForeignKey("device.Device", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    is_local = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class RuleTrigger(models.Model):

    rule = models.ForeignKey(
        Rule, on_delete=models.CASCADE, related_name="triggers", blank=True, null=True
    )
    peripheral = models.ForeignKey("peripherals.Peripherals", on_delete=models.CASCADE)
    event = models.CharField(max_length=50)
    extra_settings = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.peripheral.device.room} - {self.peripheral} - {self.event}"


class RuleCondition(models.Model):

    rule = models.ForeignKey(
        Rule, on_delete=models.CASCADE, related_name="conditions", blank=True, null=True
    )
    peripheral = models.ForeignKey(
        "peripherals.Peripherals", on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.CharField(max_length=50)
    condition = models.JSONField(default=dict)
    triggered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.peripheral} - {self.event}"


class RuleAction(models.Model):

    rule = models.ForeignKey(
        Rule, on_delete=models.CASCADE, related_name="actions", blank=True, null=True
    )
    peripheral = models.ForeignKey("peripherals.Peripherals", on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    extra_settings = models.JSONField(default=dict)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.peripheral.device.room} - {self.peripheral} - {self.action} - {self.order}"
