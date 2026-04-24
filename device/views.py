from django.db.models import QuerySet
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rules.repository import RuleRepository
from rules.serializers.rule import RuleSerializerFrontend
from .repository.device_repository import device_repository
from .repository.router_repository import RouterRepository
from .serializers.device import DeviceSerializer
from .serializers.router import RouterSerializer
from rules.models import Rule


class ListCreateRouter(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RouterSerializer

    def get_queryset(self):
        return RouterRepository.get_user_router(self.request.user)

    def perform_create(self, serializer: RouterSerializer):
        home = self.request.user.home.first()
        if not home:
            raise serializers.ValidationError("User must be assigned to a home.")
        serializer.save(home=home)


class ListCreateDevice(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        if self.request.query_params.get("unassigned", False):
            return device_repository.get_unassigned(self.request.user)
        return device_repository.get_available_for_user(self.request.user)


class RetrieveUpdateDestroyDevice(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return device_repository.get_available_for_user(self.request.user)


class ListDeviceRule(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RuleSerializerFrontend

    def get_queryset(self) -> QuerySet[Rule]:
        device_pk = self.kwargs.get("pk")
        if not device_pk:
            return Rule.objects.none()
        return RuleRepository.get_device_rules(device_pk)
