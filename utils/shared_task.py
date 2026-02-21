from celery import shared_task

from consumers.frontend.messages.messenger import FrontendMessenger
from consumers.router_message.message_event import MessageEvent
from device.serializers.device import DeviceSerializer
from rfid.models import Rfid


@shared_task
def check_add_card_request(rfid_id):
    try:
        rfid = Rfid.objects.get(id=rfid_id)
    except Rfid.DoesNotExist:
        return
    if not MessageEvent.ADD_TAG.value in rfid.pending:
        return
    try:
        rfid.pending.remove(MessageEvent.ADD_TAG.value)
    except ValueError:
        return
    rfid.save(update_fields=["pending"])
    FrontendMessenger().update_frontend(rfid.home.id, DeviceSerializer(rfid).data, 400)
