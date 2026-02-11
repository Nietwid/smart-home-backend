from django.urls import re_path
from device_consumer.device_consumer import DeviceConsumer

websocket_urlpatterns = [
    re_path(r"ws/router/(?P<mac_address>[0-9A-Fa-f:]+)/$", DeviceConsumer.as_asgi()),
]
