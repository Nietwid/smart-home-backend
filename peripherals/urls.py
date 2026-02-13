from django.urls import path
from peripherals.views import CreatePeripheral

urlpatterns = [
    path("", CreatePeripheral.as_view(), name="create-peripheral"),
]
