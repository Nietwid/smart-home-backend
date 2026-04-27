from django.urls import path

from firmware.views import FirmwareList, FirmwareDownload

urlpatterns = [
    path("", FirmwareList.as_view(), name="firmware_list"),
    path("download/", FirmwareDownload.as_view(), name="firmware_download"),
]
