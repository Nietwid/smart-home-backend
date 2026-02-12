from rest_framework.serializers import ModelSerializer
from peripherals.models import Peripherals


class PeripheralsSerializer(ModelSerializer):
    class Meta:
        model = Peripherals
        fields = "__all__"
