from rest_framework import serializers

from peripherals.models import RfidCard


class RfidCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RfidCard
        fields = "__all__"
