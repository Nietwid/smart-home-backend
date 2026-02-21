import logging

from celery import shared_task
from pydantic import ValidationError

from device.repository.device_repository import device_repository
from device_consumer.device_message import DeviceMessage
from dispatcher.command_message import CommandMessage
from dispatcher.dispatcher import device_dispatcher
from dispatcher.enums import Scope
from peripherals.repository import peripheral_repository

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
        device = None
        peripheral = None

        if message.scope == Scope.CPU:
            device = device_repository.get_device_by_mac(message.device_id)
        elif message.scope == Scope.PERIPHERAL:
            peripheral = peripheral_repository.get_by_id_with_device(
                message.peripheral_id
            )

        command_message = CommandMessage(
            scope=message.scope,
            message_type=message.message_type,
            direction=message.direction,
            message_event=message.message_event,
            payload=message.payload,
            message_id=message.message_id,
            device=device,
            peripheral=peripheral,
            home_id=home_id,
            router_mac=router_mac,
        )

        device_dispatcher.dispatch(command_message)
    except ValidationError:
        logger.error(f"Payload validation failed for message: {raw_json}")
        return
    except Exception as exc:
        # Necessary to trigger the 'auto retry_for' logic
        raise exc
