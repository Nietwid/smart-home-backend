from django.urls import path
from peripherals.views import CreatePeripheral, HandleEventAction

urlpatterns = [
    path("", CreatePeripheral.as_view(), name="create-peripheral"),
    path("trigger/", HandleEventAction.as_view(), name="trigger-peripheral"),
]
