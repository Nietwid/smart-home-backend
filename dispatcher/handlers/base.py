import logging
from abc import ABC, abstractmethod

from dispatcher.device.messages import payload
from notifier.enum import MicroserviceQueueName
from notifier.factory.microservice_notifier_factory import microservice_message_factory
from device.models import Device
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.device.messages.enum import ActionResult
from dispatcher.device.messages.payload.basic import BasicResult
from dispatcher.dispatch_result import DispatchResult
from dispatcher.tasks import check_command_timeout
from notifier.message import NotifierMessage
from notifier.factory.router_notifier_factory import router_notifier_factory
from peripherals.models import Peripherals
from redis_cache import redis_cache

from notifier.factory.frontend_notifier_factory import frontend_notifier_factory

logger = logging.getLogger(__name__)


class ActionEventBaseHandler(ABC):
    @abstractmethod
    def __call__(self, message: CommandMessage) -> DispatchResult:
        raise NotImplementedError()


class ActionIntentBaseHandler(ActionEventBaseHandler):
    save_pending: bool = True
    update_frontend_pending: bool = True
    check_command: bool = True
    check_command_timeout: int = 30

    def __call__(self, message: CommandMessage) -> DispatchResult:
        self.validate_payload(message)
        device_message = self.generate_device_message(message)
        self.save_device_message(device_message)
        device: Device = message.device

        notifications = [
            router_notifier_factory.device_message(
                router_mac=device.get_router_mac(),
                message=device_message,
            )
        ]

        if self.save_pending:
            pending = self.save_pending(device_message)
            if self.update_frontend_pending:
                notifications.append(
                    frontend_notifier_factory.update_peripheral_pending(
                        home_id=device.home.id,
                        pending=pending,
                        device_id=device.pk,
                        peripheral_id=message.peripheral.pk,
                    ),
                )
        if self.check_command:
            check_command_timeout.apply_async(
                args=(device_message.message_id,),
                countdown=self.check_command_timeout,
                queue="default",
            )

        return DispatchResult(
            notifications=notifications,
        )

    def validate_payload(self, message: CommandMessage) -> None:
        pass

    def generate_device_message(self, message: CommandMessage) -> DeviceMessage:
        return action_event_intent_builder.build_intent(message)

    def save_device_message(self, device_message: DeviceMessage) -> None:
        redis_cache.add_device_message(device_message)

    def save_pending(self, message: DeviceMessage) -> list[str]:
        return redis_cache.add_peripheral_pending(
            message.peripheral_id, message.command
        )


class ActionResultBaseHandler(ActionEventBaseHandler):
    delete_pending: bool = True
    update_frontend_pending: bool = True

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device_message = redis_cache.get_and_delete_device_message(message.message_id)
        logger.info(f"device_message: {device_message}")
        if not device_message:
            return DispatchResult()
        notifications = []
        payload: BasicResult = message.payload
        device: Device = message.device
        peripheral: Peripherals = message.peripheral
        home_id = device.home.id

        if self.delete_pending:
            pending = redis_cache.delete_peripheral_pending(
                peripheral.pk, message.command
            )
            if self.update_frontend_pending:
                notifications.extend(
                    [
                        frontend_notifier_factory.update_peripheral_pending(
                            home_id=home_id,
                            pending=pending,
                            device_id=device.pk,
                            peripheral_id=peripheral.pk,
                        ),
                    ]
                )

        if payload.status == ActionResult.REJECTED:
            notifications.append(
                frontend_notifier_factory.display_toaster(
                    home_id=home_id,
                    message=f"Unable to {message.command} peripheral on {device.name}",
                )
            )
        return DispatchResult(notifications=notifications)


class EventIntentBaseHandler(ActionEventBaseHandler):
    send_command: bool = True
    update_frontend_peripheral_state: bool = False
    exchange: str = None
    routing_key: str = None
    history_queue: MicroserviceQueueName = None

    def __call__(self, message: CommandMessage) -> DispatchResult:
        notifications = []
        commands = []
        device: Device = message.device
        peripheral: Peripherals = message.peripheral

        self.update_peripheral_state(peripheral, message.payload)
        if self.exchange is not None and self.routing_key is not None:
            notifications.append(
                microservice_message_factory.log_event(
                    peripheral=peripheral,
                    event_type=message.command,
                    payload=message.payload,
                    exchange=self.exchange,
                    routing_key=self.routing_key,
                )
            )

        if self.update_frontend_peripheral_state:
            notifications.append(
                frontend_notifier_factory.update_peripheral_state(
                    peripheral=peripheral
                ),
            )

        if self.send_command:
            commands.extend(
                device.get_event_request(
                    peripheral=message.peripheral,
                    event_type=message.command,
                    payload=message.payload,
                )
            )

        notifications.extend(self.get_extra_notification(message))
        commands.extend(self.get_extra_commands(message))

        return DispatchResult(notifications=notifications, commands=commands)

    def get_extra_notification(self, message: CommandMessage) -> list[NotifierMessage]:
        return []

    def get_extra_commands(self, message: CommandMessage) -> list[CommandMessage]:
        return []

    def update_peripheral_state(self, peripheral: Peripherals, state: dict) -> None:
        pass
