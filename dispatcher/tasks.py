import logging
from celery import shared_task
from pydantic import ValidationError

from dispatcher.device.messages.device_message import DeviceMessage
from device.repository.device_repository import device_repository
from dispatcher.device.messages.enum import Scope
from dispatcher.processor.action_event_command import action_event_command_processor
from dispatcher.command_message.factory import command_message_factory
from notifier.frontend_notifier_factory import frontend_notifier_factory
from peripherals.repository import peripheral_repository
from redis_cache import redis_cache
from notifier.notifier import notifier

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def handle_device_message_task(
    self, raw_json: str, home_id: int, router_mac: str
) -> None:
    """
    Asynchronously processes incoming hardware events from the message broker.

    This task acts as a bridge between the WebSocket consumer and the business
    logic layer. It validates the raw JSON payload and dispatches it to the
    appropriate hardware handler.

    Args:
        raw_json (str): The raw JSON string received from the device.
        home_id (int):
        router_mac (str):
    Returns:
        None

    Raises:
        ValidationError: If the raw_json does not match the DeviceMessage schema.
        Exception: Re-raises exceptions to trigger Celery's auto retry mechanism.
    """
    try:
        message = DeviceMessage.model_validate_json(raw_json)
        print(f"TASK message: {message}")
        command_message = command_message_factory.from_device_message(
            message, home_id, router_mac
        )
    except ValidationError as e:
        logger.error(f"Payload validation failed for message: {raw_json} : {e}")
        return
    except Exception as exc:
        logger.error(f"Error processing message. exc: {exc}")
        # Necessary to trigger the 'auto retry_for' logic
        raise exc
    action_event_command_processor(command_message)


@shared_task(
    name="check_pending_command_timeout",
    bind=True,
    ignore_result=True,
    default_retry_delay=15,
    max_retries=3,
)
def check_command_timeout(self, message_id: str):
    message = redis_cache.get_device_message_and_delete(message_id)
    if not message:
        return

    if message.scope == Scope.PERIPHERAL:
        peripheral = peripheral_repository.get_by_id_with_device(message.peripheral_id)
        home_id = peripheral.device.home.id
        device_name = peripheral.device.name
        pending = redis_cache.delete_device_pending(
            message.peripheral_id, message.command, peripheral=True
        )
        notifications = [
            frontend_notifier_factory.update_peripheral_pending(
                home_id=peripheral.device.home.id,
                pending=pending,
                device_id=peripheral.device.pk,
                peripheral_id=message.peripheral_id,
            ),
        ]
    elif message.scope == Scope.CPU:
        device = device_repository.get_by_mac(mac=message.device_id)
        home_id = device.home.pk
        device_name = device.name
        pending = redis_cache.delete_device_pending(device.pk, message.command)
        notifications = [
            frontend_notifier_factory.update_device_pending(
                home_id=device.home.id,
                pending=pending,
                device_id=device.pk,
            ),
        ]
    else:
        logger.error(f"Invalid scope: {message.scope}")
        return

    error_message = f"Device {device_name} unreachable"
    notifications.append(
        frontend_notifier_factory.display_toaster(
            home_id=home_id, message=error_message
        )
    )
    notifier.notify(notifications)
