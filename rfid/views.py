from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response

from consumers.frontend.messages.messenger import FrontendMessenger
from consumers.router_message.builders.rfid import add_tag_request
from consumers.router_message.message_event import MessageEvent
from consumers.device.messenger import DeviceMessenger
from device.serializers.device import DeviceSerializer
from .serializer import CardSerializer
from .models import Card, Rfid


class RfidListCreate(ListCreateAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Rfid.objects.filter(room__user=self.request.user)


class RfidRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Rfid.objects.filter(room__user=self.request.user)


class CardDestroy(DestroyAPIView):

    def get_queryset(self):
        return Card.objects.filter(
            rfid__room__user=self.request.user, id=self.kwargs["pk"]
        )

    def delete(self, request, *args, **kwargs):
        rfid = self.get_object().rfid
        home_id = rfid.home.id
        super().delete(request, *args, **kwargs)
        FrontendMessenger().update_frontend(home_id, DeviceSerializer(rfid).data, 200)
        return Response(status=204)


class CardListCreate(ListCreateAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        rfid = get_object_or_404(
            Rfid, id=self.request.data.get("rfid_id", 0), room__user=self.request.user
        )
        return rfid

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        rfid = validated_data["rfid"]

        if not MessageEvent.ADD_TAG.value in rfid.pending:
            rfid.pending.append(MessageEvent.ADD_TAG.value)
            rfid.save()

        serializer_data = DeviceSerializer(rfid).data
        request = add_tag_request(rfid.mac, validated_data["name"])
        DeviceMessenger().send(rfid.get_router_mac(), request)

        # settings = Settings()
        # check_add_card_request.apply_async(
        #     (rfid.id,), countdown=settings.get(TimeSettingKey.ADD_TAG_WAIT, 20)
        # )
        return Response(serializer_data, 200)
