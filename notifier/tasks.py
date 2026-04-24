import os
import pika
from django.db import transaction
from celery import shared_task
from django.utils import timezone
from pika.exceptions import AMQPError
from torch.distributed.elastic.utils import logging

from consumers.models import RouterOutbox, MessageStatus, RabbitOutbox
from consumers.router.message.message import DeviceRouterMessage
from consumers.router.messenger import router_messenger
from dispatcher.device.messages.device_message import DeviceMessage
logger = logging.get_logger(__name__)

@shared_task(ignore_result=True)
def process_router_outbox_task():
    while True:
        with transaction.atomic():
            messages = list(
                RouterOutbox.objects.select_for_update(skip_locked=True).filter(
                    status=MessageStatus.PENDING
                )[:50]
            )

            if not messages:
                return

            for msg in messages:
                if msg.expired_at < timezone.now():
                    msg.status = MessageStatus.EXPIRED
                    continue

                try:
                    payload = DeviceMessage.model_validate_json(msg.payload)
                except Exception as e:
                    logger.error(
                        f"Payload validation failed for message: {msg.payload} : {e}"
                    )
                message = DeviceRouterMessage(payload=payload)
                router_messenger.send(msg.router_mac, message)
                msg.status = MessageStatus.DELIVERED

            RouterOutbox.objects.bulk_update(messages, ["status"])


@shared_task(ignore_result=True)
def send_microservice_notification():
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    if not rabbitmq_url:
        return
    try:
        with pika.BlockingConnection(pika.URLParameters(rabbitmq_url)) as connection:
            channel = connection.channel()
            channel.confirm_delivery()
            exchanges = set()
            while True:
                with transaction.atomic():
                    messages = RabbitOutbox.objects.select_for_update(skip_locked=True).filter(status=MessageStatus.PENDING)[:50]
                    if not messages.exists():
                        return
                    msg_ids = [m.pk for m in messages]
                    RabbitOutbox.objects.filter(id__in=msg_ids).update(status=MessageStatus.SENDING)

                for message in messages:
                    try:
                        if message.exchange not in exchanges:
                            channel.exchange_declare(exchange=message.exchange, exchange_type="topic")
                            exchanges.add(message.exchange)
                        channel.basic_publish(
                            exchange=message.exchange,
                            routing_key=message.routing_key,
                            body=message.payload,
                            properties=pika.BasicProperties(delivery_mode=1)
                        )
                    except Exception as e:
                        logger.error(f"Failed to publish message {message.payload}: {e}")
                    message.status = MessageStatus.DELIVERED
                if msg_ids:
                    RabbitOutbox.objects.filter(id__in=msg_ids).update(status=MessageStatus.DELIVERED)
    except AMQPError as e:
        logger.error(f"RabbitMQ error: {e}")