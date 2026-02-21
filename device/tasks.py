from aquarium.models import Aquarium
from aquarium.serializer import AquariumSerializerDevice
from consumers.frontend.messages.messenger import FrontendMessenger
from consumers.router_message.builders.basic import set_settings_request
from consumers.router_message.messenger import DeviceMessenger
from device.serializers.device import DeviceSerializer
from utils.check_hour_in_range import check_hour_in_range
from celery import shared_task


@shared_task
def check_devices():
    aquariums = Aquarium.objects.all()
    for aquarium in aquariums:
        to_save = []
        if not aquarium.mode:
            continue
        led_mode = check_hour_in_range(aquarium.led_start, aquarium.led_stop)
        fluo_mode = check_hour_in_range(aquarium.fluo_start, aquarium.fluo_stop)
        if led_mode != aquarium.led_mode:
            aquarium.led_mode = led_mode
            to_save.append("led_mode")
        if fluo_mode != aquarium.fluo_mode:
            aquarium.fluo_mode = fluo_mode
            to_save.append("fluo_mode")
        if not to_save:
            continue
        aquarium.save(update_fields=to_save)

        message = set_settings_request(
            aquarium.mac, AquariumSerializerDevice(aquarium).data
        )
        DeviceMessenger().send(aquarium.get_router_mac(), message)
        FrontendMessenger().update_frontend(
            aquarium.home.id, DeviceSerializer(aquarium).data, 200
        )
