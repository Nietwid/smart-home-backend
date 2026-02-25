from consumers.device.messenger import DeviceMessenger
from device_registry import DeviceRegistry
from consumers.router_message.builders.basic import set_settings_request


def send_set_settings_request(instance):
    serializer = DeviceRegistry().get_serializer_device(instance.fun)
    new_data: dict = serializer(instance).data
    request = set_settings_request(instance.mac, new_data)
    DeviceMessenger().send(instance.get_router_mac(), request)
