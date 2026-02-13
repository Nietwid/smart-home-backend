from rest_framework.serializers import Serializer
from hardware.pin.serializer import BasicPinSerializer


class PwmConfigSerializer(BasicPinSerializer): ...


class PwmStateSerializer(Serializer): ...
