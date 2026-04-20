from django.urls import path, re_path
from consumers.frontend.consumer import UserConsumer
from consumers.router.consumer import RouterConsumer

websocket_urlpatterns = [
    path(r"ws/user/<str:token>/", UserConsumer.as_asgi()),
    re_path(r"ws/router/(?P<mac_address>[0-9A-Fa-f:]+)/$", RouterConsumer.as_asgi()),
]
