from typing import TYPE_CHECKING
from django.db import models

from dispatcher.device.messages.enum import MessageCommand
from hardware.registry import HARDWARE_REGISTRY

from room.models import Room
from rules.models import RuleCondition

from user.models import Home

if TYPE_CHECKING:
    from dispatcher.command_message.message import CommandMessage


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
    mac = models.CharField(max_length=100, db_index=True, unique=True)
    wifi_strength = models.IntegerField(default=0)
    is_online = models.BooleanField(default=False)
    firmware_version = models.FloatField(default=1.0)
    chip_type = models.CharField(
        max_length=100, choices=ChipType, default=ChipType.ESP32
    )
    required_action = models.JSONField(default=list, blank=True, null=True)

    svg_id = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_event_request(
        self, peripheral, event_type: MessageCommand, payload
    ) -> "list[CommandMessage]":
        from dispatcher.command_message.factory import command_message_factory
        from rules.models import Rule

        rules = Rule.objects.filter(
            device=self,
            enabled=True,
            is_local=False,
            triggers__peripheral=peripheral,
            triggers__event=event_type,
        ).prefetch_related("conditions", "actions", "actions__peripheral")
        home_id = self.home.id
        router_mac = self.home.router.mac
        command_messages = []
        for rule in rules:
            if self._check_conditions(rule.conditions.all(), payload):
                for action in rule.actions.all().order_by("order"):
                    command_messages.append(
                        command_message_factory.get_commands_from_rule(
                            self, home_id, router_mac, action
                        )
                    )
        return command_messages

    def get_router(self):
        return Router.objects.get(home=self.home)

    def get_router_mac(self):
        return (
            Router.objects.filter(home=self.home).values_list("mac", flat=True).first()
        )

    def extra_settings(self):
        return {}

    def make_intent(self, data: dict) -> None:
        return

    def _check_conditions(self, conditions: list[RuleCondition], payload) -> bool:
        if not conditions:
            return True

        for cond in conditions:
            hw_class = HARDWARE_REGISTRY.get(cond.peripheral.name)
            if not hw_class:
                raise Exception(f"Unsupported device type: {cond.peripheral.name}")

            attr_name = hw_class.event_to_attr.get(cond.event)
            if not attr_name:
                raise Exception(f"Unsupported event: {cond.event}")

            current_value = getattr(payload, attr_name)
            if current_value is None:
                raise Exception(f"Attribute {attr_name} not found in payload")

            cond_type = cond.condition.get("type")
            if cond_type == "numeric":
                is_met = self._evaluate_numeric(current_value, cond)
            elif cond_type == "boolean":
                is_met = self._evaluate_boolean(current_value, cond)
            else:
                raise Exception(f"Unknown condition type: {cond_type}")
            if not is_met:
                return False
        return True

    def _evaluate_numeric(self, current_value: float, cond: RuleCondition) -> bool:
        import operator

        ops = {
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
        }

        op_str = cond.condition.get("operator")
        threshold = cond.condition.get("value")
        hysteresis = cond.condition.get("hysteresis", 0.0)
        last_triggered = cond.triggered

        if hysteresis == 0.0 or not last_triggered:
            is_currently_true = ops[op_str](current_value, threshold)
        elif op_str in [">", ">="]:
            is_currently_true = current_value > (threshold - hysteresis)
        else:
            is_currently_true = current_value < (threshold + hysteresis)

        if is_currently_true != last_triggered:
            cond.triggered = is_currently_true
            cond.save(update_fields=["triggered"])
            return is_currently_true
        return False

    def _evaluate_boolean(self, current_value: bool, cond: RuleCondition) -> bool:
        expected = cond.condition.get("state")
        is_currently_true = current_value == expected
        if is_currently_true != cond.triggered:
            cond.triggered = is_currently_true
            cond.save(update_fields=["triggered"])
            return is_currently_true

        return False
