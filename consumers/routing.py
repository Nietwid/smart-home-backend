from django.urls import re_path, path
from .frontend import UserConsumer
from .camera import CameraConsumer

websocket_urlpatterns = [
    path(r"ws/user/<str:token>/", UserConsumer.as_asgi()),
    path(r"ws/camera/<str:token>/<int:pk>/", CameraConsumer.as_asgi()),
]
