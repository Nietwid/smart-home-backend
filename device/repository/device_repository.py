from typing import Optional

from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q, QuerySet
from device.models import Device, ChipType
from user.models import Home


class DeviceRepository:

    def get_unassigned(self, user: AbstractBaseUser) -> QuerySet[Device]:
        return Device.objects.filter(
            home__users=user, room__isnull=True
        ).prefetch_related("peripherals")

    def get_available_for_user(self, user: AbstractBaseUser) -> QuerySet[Device]:
        return Device.objects.filter(
            Q(home__users=user), Q(room__user=user) | Q(room__visibility="PU")
        ).prefetch_related("peripherals")

    def get_by_id(self, device_id: int) -> Optional[Device]:
        return Device.objects.filter(id=device_id).first()

    def get_by_mac(self, mac: str) -> Device:
        return Device.objects.select_related("home").get(mac=mac)

    def create(self, home_id: int, mac: str, chip_type: ChipType) -> Device:
        return Device.objects.create(home=home_id, mac=mac, chip_type=chip_type)

    def get_by_mac_or_create(
        self, home_id: int, mac: str, chip_type: ChipType
    ) -> Device:
        device, created = Device.objects.get_or_create(
            mac=mac,
            defaults={"chip_type": chip_type, "home": Home.objects.get(pk=home_id)},
        )
        return device


device_repository = DeviceRepository()
