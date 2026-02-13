from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from peripherals.serializers import PeripheralSerializer


class CreatePeripheral(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PeripheralSerializer
