from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q, QuerySet
from typing import Optional
from django.db.models import Prefetch
from device.models import Device
from peripherals.models import Peripherals


class DeviceRepository:

    @staticmethod
    def get_unassigned(user: AbstractBaseUser) -> QuerySet[Device]:
        return Device.objects.filter(
            home__users=user, room__isnull=True
        ).prefetch_related("peripherals")

    @staticmethod
    def get_available_for_user(user: AbstractBaseUser) -> QuerySet[Device]:
        return Device.objects.filter(
            Q(home__users=user),
            Q(room__user=user) | Q(room__visibility="PU"),
        ).prefetch_related("peripherals")

    @staticmethod
    def get_device_with_peripheral_by_mac(
        mac: str, peripheral_id: int
    ) -> Optional[Device]:
        """
        Returns a Device with a specific peripheral by its ID.

        Args:
            mac (str): MAC address of the Device.
            peripheral_id (int): ID of the Peripheral to prefetch.

        Returns:
            Optional[Device]: The Device object with the specified peripheral
        """
        prefetch = Prefetch(
            "peripherals",
            queryset=Peripherals.objects.filter(id=peripheral_id),
        )
        return Device.objects.filter(mac=mac).prefetch_related(prefetch).first()
