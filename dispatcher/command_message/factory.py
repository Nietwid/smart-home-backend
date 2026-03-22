from dispatcher.device.messages.enum import MessageCommand
from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.payload.cpu import (
    UpdatePeripheralIntentPayload,
    StartSyncPayload,
    UpdateRuleIntentPayload,
)
from dispatcher.device.messages.payload.enum import StartSyncType
from peripherals.action_event_frontend_message import ActionEventFrontendMessage
from peripherals.repository import peripheral_repository
from device.repository.device_repository import device_repository
from device.models import Device


class CommandMessageFactory:
    def from_frontend_message(
        self, message: ActionEventFrontendMessage
    ) -> CommandMessage:
        peripheral = None

        if message.scope == Scope.CPU:
            device = device_repository.get_by_mac(mac=message.device_id)
            home_id = device.home.pk
            router_mac = device.home.router.mac
        elif message.scope == Scope.PERIPHERAL:
            peripheral = peripheral_repository.get_by_id_with_device(
                message.peripheral_id
            )
            device = peripheral.device
            home_id = peripheral.device.home.pk
            router_mac = peripheral.device.home.router.mac
        else:
            raise ValueError(f"Invalid scope: {message.scope}")

        return CommandMessage(
            scope=message.scope,
            type=message.type,
            direction=MessageDirection.INTENT,
            command=message.command,
            payload=message.payload,
            device=device,
            peripheral=peripheral,
            home_id=home_id,
            router_mac=router_mac,
        )

    def from_device_message(
        self, message: DeviceMessage, home_id: int, router_mac: str
    ) -> CommandMessage:
        """
        Builds a CommandMessage from a raw DeviceMessage.

        Resolves and attaches related domain entities (Device or Peripheral)
        based on message scope and event type, so handlers receive
        a fully prepared execution context.
        """

        device = None
        peripheral = None

        if message.scope == Scope.CPU:
            if message.command == MessageCommand.DEVICE_CONNECT:
                device = device_repository.get_by_mac_or_create(
                    home_id=home_id,
                    mac=message.device_id,
                    chip_type=message.payload.chip_type,
                )
            else:
                try:
                    device = device_repository.get_by_mac(mac=message.device_id)
                except Device.DoesNotExist:
                    print(f"{message=}")
        elif message.scope == Scope.PERIPHERAL:
            peripheral = peripheral_repository.get_by_id_with_device(
                message.peripheral_id
            )
            device = peripheral.device
        return CommandMessage(
            scope=message.scope,
            type=message.type,
            direction=message.direction,
            command=message.command,
            payload=message.payload,
            message_id=message.message_id,
            device=device,
            peripheral=peripheral,
            home_id=home_id,
            router_mac=router_mac,
        )

    def sync_start(self, device: Device, sync_type: StartSyncType) -> CommandMessage:
        home_id = device.home.pk
        router_mac = device.home.router.mac
        return CommandMessage(
            scope=Scope.CPU,
            type=MessageType.ACTION,
            direction=MessageDirection.INTENT,
            command=MessageCommand.SYNC_START,
            home_id=home_id,
            router_mac=router_mac,
            payload=StartSyncPayload(sync_type=sync_type),
            device=device,
        )

    def update_peripheral(self, device: Device, peripheral_id: int) -> CommandMessage:
        home_id = device.home.pk
        router_mac = device.home.router.mac
        return CommandMessage(
            scope=Scope.CPU,
            type=MessageType.ACTION,
            direction=MessageDirection.INTENT,
            command=MessageCommand.UPDATE_PERIPHERAL,
            home_id=home_id,
            router_mac=router_mac,
            payload=UpdatePeripheralIntentPayload(peripheral_id=peripheral_id),
            device=device,
        )

    def update_rule(self, device: Device, rule_id: int) -> CommandMessage:
        home_id = device.home.pk
        router_mac = device.home.router.mac
        return CommandMessage(
            scope=Scope.CPU,
            type=MessageType.ACTION,
            direction=MessageDirection.INTENT,
            command=MessageCommand.UPDATE_RULE,
            home_id=home_id,
            router_mac=router_mac,
            payload=UpdateRuleIntentPayload(rule_id=rule_id),
            device=device,
        )

    def sync_end(self, device: Device, sync_type: StartSyncType) -> CommandMessage:
        home_id = device.home.pk
        router_mac = device.home.router.mac
        return CommandMessage(
            scope=Scope.CPU,
            type=MessageType.ACTION,
            direction=MessageDirection.INTENT,
            command=MessageCommand.SYNC_END,
            home_id=home_id,
            router_mac=router_mac,
            payload=StartSyncPayload(sync_type=sync_type),
            device=device,
        )

    def restart(self, device: Device) -> CommandMessage:
        home_id = device.home.pk
        router_mac = device.home.router.mac
        return CommandMessage(
            scope=Scope.CPU,
            type=MessageType.ACTION,
            direction=MessageDirection.INTENT,
            command=MessageCommand.RESTART,
            home_id=home_id,
            router_mac=router_mac,
            payload={},
            device=device,
        )


command_message_factory = CommandMessageFactory()
