from django.urls import path
from .frontend import UserConsumer

websocket_urlpatterns = [
    path(r"ws/user/<str:token>/", UserConsumer.as_asgi()),
]
