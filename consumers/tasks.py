from celery import shared_task
from django.utils import timezone


from device.models import Router, Device
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.notifier import notifier


@shared_task
def deactivate_all_device(router_id: int):
    try:
        router = Router.objects.get(pk=router_id)
    except Router.DoesNotExist:
        return
    home_id = router.home.pk
    devices = Device.objects.filter(home=router.home, is_online=True)
    messages = [
        frontend_notifier_factory.update_router(
            home_id=home_id,
            data=RouterSerializer(router).data,
        )
    ]

    for device in devices:
        device.is_online = False
        device.last_seen = timezone.now()
        device.save(update_fields=["is_online", "last_seen"])
        messages.append(
            frontend_notifier_factory.update_device(
                home_id, DeviceSerializer(device).data
            )
        )

    notifier.notify(messages)
