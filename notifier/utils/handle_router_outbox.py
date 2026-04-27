from datetime import timedelta
from django.utils import timezone
from consumers.models import RouterOutbox
from notifier.message import RouterNotifierData
from notifier.tasks import process_router_outbox_task


def handle_router_outbox(message: RouterNotifierData):
    message, created = RouterOutbox.objects.get_or_create(
        router_mac=message.router_mac,
        external_id=message.data.message_id,
        defaults={
            "expired_at": timezone.now() + timedelta(seconds=20),
            "payload": message.data.payload.model_dump_json(),
        },
    )
    if not created:
        return
    process_router_outbox_task.delay()
