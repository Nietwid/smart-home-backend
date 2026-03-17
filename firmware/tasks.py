from celery import shared_task

from firmware.models import FirmwareDevice
from django.db.models import Max, Q


@shared_task
def delete_old_firmware():
    # devices_type = DeviceRegistry().devices
    # max_values = (
    #     FirmwareDevice.objects.filter(to_device__in=devices_type)
    #     .values("to_device")
    #     .annotate(max_value=Max("version"))
    # )
    # exclude_q = Q()
    # for value in max_values:
    #     exclude_q |= Q(to_device=value["to_device"], version=value["max_value"])
    # to_delete = FirmwareDevice.objects.all().exclude(exclude_q)
    # for instance in to_delete:
    #     instance.file.delete()
    # to_delete.delete()
    pass
