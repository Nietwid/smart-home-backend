from django.urls import path
from peripherals.views import (
    CreatePeripheral,
    HandleEventAction,
    GetAllPeripheralRfidCards,
)

urlpatterns = [
    path("", CreatePeripheral.as_view(), name="create-peripheral"),
    path("trigger/", HandleEventAction.as_view(), name="trigger-peripheral"),
    path(
        "rfid-card/<int:pk>/", GetAllPeripheralRfidCards.as_view(), name="all-rfid-card"
    ),
]
