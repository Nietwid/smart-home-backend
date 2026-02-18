import logging

from celery import shared_task
from pydantic import ValidationError

from consumers.router_message.device_message import DeviceMessage
from device_consumer.services.process_device_message import process_device_message

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def handle_device_message_task(self, raw_json: str):
    """
    Asynchronously processes incoming hardware events from the message broker.

    This task acts as a bridge between the WebSocket consumer and the business
    logic layer. It validates the raw JSON payload and dispatches it to the
    appropriate hardware handler.

    Args:
        raw_json (str): The raw JSON string received from the device.

    Returns:
        None

    Raises:
        ValidationError: If the raw_json does not match the DeviceMessage schema.
        Exception: Re-raises exceptions to trigger Celery's auto retry mechanism.
    """
    try:
        message = DeviceMessage.model_validate_json(raw_json)
        process_device_message(message)
    except ValidationError:
        logger.error(f"Payload validation failed for message: {raw_json}")
        return
    except Exception as exc:
        # Necessary to trigger the 'auto retry_for' logic
        raise exc
