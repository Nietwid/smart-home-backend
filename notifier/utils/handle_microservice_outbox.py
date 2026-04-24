from consumers.models import RabbitOutbox
from notifier.message import MicroserviceNotifierData
from notifier.tasks import send_microservice_notification


def handle_microservice_outbox(message: MicroserviceNotifierData):
    message, created = RabbitOutbox.objects.get_or_create(
        external_id=message.data.message_id,
        exchange=message.exchange,
        routing_key=message.routing_key,
        defaults={
            "payload": message.data.model_dump_json(),
        },
    )
    if not created:
        return

    send_microservice_notification.delay()
