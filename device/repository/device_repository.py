from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q, QuerySet
from device.models import Device


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
