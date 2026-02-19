from typing import Optional

from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q, QuerySet
from device.models import Device


class DeviceRepository:

    def get_unassigned(self, user: AbstractBaseUser) -> QuerySet[Device]:
        return Device.objects.filter(
            home__users=user, room__isnull=True
        ).prefetch_related("peripherals")

    def get_available_for_user(self, user: AbstractBaseUser) -> QuerySet[Device]:
        return Device.objects.filter(
            Q(home__users=user),
            Q(room__user=user) | Q(room__visibility="PU"),
        ).prefetch_related("peripherals")

    def get_by_id(self, device_id: int) -> Optional[Device]:
        return Device.objects.filter(id=device_id).first()

    def get_by_mac(self, mac: str) -> Optional[Device]:
        return Device.objects.filter(mac=mac).first()


device_repository = DeviceRepository()
