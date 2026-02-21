from consumers.frontend.messages.messenger import FrontendMessenger
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_event import MessageEvent
from consumers.events.base_event import BaseEventResponse
from device.serializers.device import DeviceSerializer
from rfid.models import Rfid, Card


class AddTagEvent(BaseEventResponse):

    def handle_response(self, consumer, message: DeviceMessage):
        uid = message.payload.uid
        name = message.payload.name
        if not uid:
            return

        device = self._get_device(message.device_id)
        if not device:
            return

        rfid = Rfid.objects.get(pk=device.id)
        status = 400
        if uid:
            cards = Card.objects.filter(uid=uid)
            if cards.exists():
                status = 409
            else:
                Card.objects.create(
                    rfid=rfid,
                    uid=uid,
                    name=name,
                )
                status = 201
        if MessageEvent.ADD_TAG.value in rfid.pending:
            rfid.pending.remove(MessageEvent.ADD_TAG.value)
            rfid.save(update_fields=["pending"])
        FrontendMessenger().update_frontend(
            rfid.home.id, DeviceSerializer(rfid).data, status
        )
