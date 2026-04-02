from typing import TYPE_CHECKING
from django.db import models

from dispatcher.device.messages.enum import MessageCommand

from room.models import Room

from user.models import Home

if TYPE_CHECKING:
    from peripherals.models import Peripherals
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
        self, peripheral, event_type: MessageCommand
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
            if self._check_conditions(rule.conditions.all()):
                for action in rule.actions.all().order_by("order"):
                    command_messages.append(
                        command_message_factory.get_commands_from_rule(
                            self, home_id, router_mac, action
                        )
                    )
        print(command_messages)
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

    def _check_conditions(self, conditions) -> bool:
        return True
        # for cond in conditions:
        #     current_value = self.get_peripheral_state(cond.peripheral)
        #
        #     operators = {
        #         "==": lambda a, b: str(a) == str(b),
        #         ">": lambda a, b: float(a) > float(b),
        #         "<": lambda a, b: float(a) < float(b),
        #         "!=": lambda a, b: str(a) != str(b),
        #     }
        #
        #     op_func = operators.get(cond.operator)
        #     if not op_func or not op_func(current_value, cond.value):
        #         return False
        #
        # return True
