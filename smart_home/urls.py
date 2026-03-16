from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user.urls")),
    path("api/room/", include("room.urls")),
    path("api/lamp/", include("lamp.urls")),
    path("api/stairs/", include("stairs.urls")),
    path("api/device/", include("device.urls")),
    path("api/rfid/", include("rfid.urls")),
    path("api/event/", include("event.urls")),
    path("api/cameras/", include("camera.urls")),
    path("api/temperature/", include("temperature.urls")),
    path("api/firmware/", include("firmware.urls")),
    path("api/peripherals/", include("peripherals.urls")),
    path("api/rule/", include("rules.urls")),
]
