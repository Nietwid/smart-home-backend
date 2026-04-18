from django.urls import path

from firmware.views import FirmwareList, FirmwareDownload

urlpatterns = [
    # path("firmware/", views.download_firmware, name="download_firmware"),
    path("", FirmwareList.as_view(), name="firmware_list"),
    path("download/", FirmwareDownload.as_view(), name="firmware_download"),
]
