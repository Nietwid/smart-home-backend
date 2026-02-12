from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from device.models import Device, Router
from device_registry import DeviceRegistry
from room.models import Room
from utils.get_available_for_user_device import get_available_for_user_device
from .repository.device_repository import DeviceRepository
from .serializers.device import DeviceSerializer
from .serializers.router import RouterSerializer


class ListCreateRouter(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RouterSerializer

    def get_queryset(self):
        return get_list_or_404(Router, home__users=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data["home"] = request.user.home.all().first().id
        return super().create(request, *args, **kwargs)


class ListCreateDevice(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        if self.request.query_params.get("unassigned", False):
            return DeviceRepository.get_unassigned(self.request.user)
        return DeviceRepository.get_available_for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        room = get_object_or_404(
            Room, Q(user=self.request.user) | Q(visibility="PU"), pk=data["room_id"]
        )
        device = get_object_or_404(
            Device, home__users=self.request.user, pk=data["device_id"]
        )
        device.room = room
        device.save(update_fields=["room"])
        return Response(data, 201)


class RetrieveUpdateDestroyDevice(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return get_available_for_user_device(Device, self.request.user)


class UpdateButtonType(UpdateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_available_for_user_device(Device, self.request.user)
