from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from consumers.router_message.messenger import DeviceMessenger
from peripherals.serializers import PeripheralSerializer


class CreatePeripheral(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PeripheralSerializer
