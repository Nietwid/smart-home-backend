import logging

from celery import shared_task
from pydantic import ValidationError

from dispatcher.messages.device_message import DeviceMessage
from dispatcher.context.builder import context_builder
from dispatcher.dispatchers.device_dispatcher import device_dispatcher

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
        context = context_builder.build(message, home_id, router_mac)
        device_dispatcher.dispatch(message, context)
    except ValidationError:
        logger.error(f"Payload validation failed for message: {raw_json}")
        return
    except Exception as exc:
        # Necessary to trigger the 'auto retry_for' logic
        raise exc
