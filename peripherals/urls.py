from django.urls import path
from peripherals.views import (
    CreatePeripheral,
    HandleEventAction,
    GetAllPeripheralRfidCards,
    CardDestroyAPIView,
    RetrieveDestroyPeripheral,
)

urlpatterns = [
    path("", CreatePeripheral.as_view(), name="create-peripheral"),
    path(
        "<int:pk>/",
        RetrieveDestroyPeripheral.as_view(),
        name="retrieve-destroy-peripheral",
    ),
    path("trigger/", HandleEventAction.as_view(), name="trigger-peripheral"),
    path("<int:pk>/card/", GetAllPeripheralRfidCards.as_view(), name="all-rfid-card"),
    path(
        "<int:peripheral_id>/card/<int:pk>/",
        CardDestroyAPIView.as_view(),
        name="delete-rfid-card",
    ),
]
