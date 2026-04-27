from datetime import timedelta
from django.utils import timezone

from consumers.models import RouterOutbox, MessageStatus, RouterInbox
from consumers.router.message.message import AckRouterMessage, DeviceRouterMessage
from consumers.tasks import deactivate_all_device
from device.serializers.router import RouterSerializer
from dispatcher.device.messages.enum import (
    MessageDirection,
    MessageCommand,
    Scope,
    MessageType,
)
from dispatcher.tasks import process_device_message_task
from notifier.factory.frontend_notifier_factory import frontend_notifier_factory
from notifier.message import RouterNotifierData
from notifier.notifier import notifier
from dispatcher.device.messages.device_message import DeviceMessage
from notifier.factory.router_notifier_factory import router_notifier_factory
from device.models import Router


class RouterService:
    def __init__(self, router):
        self.router = router

    @staticmethod
    def handle_connect(mac: str) -> Router | None:
        try:
            router = Router.objects.select_related("home").get(mac=mac)
        except Router.DoesNotExist:
            return None
        router.last_seen = timezone.now()
        router.is_online = True
        router.save(update_fields=["last_seen", "is_online"])
        return router

    def handle_disconnect(self):
        self.router.last_seen = timezone.now()
        self.router.is_online = False
        self.router.save(update_fields=["last_seen", "is_online"])
        deactivate_all_device.delay(self.router.pk)

    def handle_ack_received(self, packet: AckRouterMessage):
        try:
            message = RouterOutbox.objects.get(external_id=packet.message_id)
        except RouterOutbox.DoesNotExist:
            return
        message.status = MessageStatus.DELIVERED
        message.save(update_fields=["status"])

    def handle_device_message(self, packet: DeviceRouterMessage):
        message, created = RouterInbox.objects.get_or_create(
            router_mac=self.router.mac,
            external_id=packet.message_id,
            defaults={
                "expired_at": timezone.now() + timedelta(seconds=20),
                "payload": packet.payload.model_dump_json(),
                "home_id": self.router.home.pk,
            },
        )
        notifier.notify(
            [
                RouterNotifierData(
                    router_mac=self.router.mac,
                    data=AckRouterMessage(message_id=message.external_id),
                )
            ]
        )
        if not created:
            return
        process_device_message_task.delay()

    def notify_frontend(self):
        data = RouterSerializer(self.router).data
        notifier.notify(
            [
                frontend_notifier_factory.update_router(
                    home_id=self.router.home.pk, data=data
                )
            ]
        )

    def send_get_connected_message(self):
        device_message = DeviceMessage(
            direction=MessageDirection.INTENT,
            command=MessageCommand.GET_CONNECTED_DEVICES,
            type=MessageType.ACTION,
            scope=Scope.CPU,
            device_id="00:00:00:00:00:00",
            peripheral_id=0,
            payload={},
        )
        notifications = [
            router_notifier_factory.device_message(
                router_mac=self.router.mac,
                message=device_message,
            ),
        ]
        notifier.notify(notifications)
