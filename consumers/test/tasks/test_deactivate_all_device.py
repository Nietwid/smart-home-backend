from device.models import Device
from consumers.test.tasks.conftest import *
from consumers.tasks import deactivate_all_device


def test_deactivate_all_device_updates_db_and_notifies(db, mock_notifier, router):
    # Given
    devices_online = [
        Device.objects.create(home=router.home, is_online=True, mac="AA"),
        Device.objects.create(home=router.home, is_online=True, mac="BB"),
    ]
    device_offline = Device.objects.create(home=router.home, is_online=False, mac="CC")

    # When
    deactivate_all_device(router.pk)

    # Then
    for d in devices_online:
        d.refresh_from_db()
        assert d.is_online is False
        assert d.last_seen is not None

    device_offline.refresh_from_db()
    assert device_offline.is_online is False

    assert mock_notifier.called
    sent_messages = mock_notifier.call_args[0][0]
    assert len(sent_messages) == 3


def test_deactivate_all_device_router_not_exists(db, mock_notifier):
    # Given
    non_existent_id = 99999

    # When
    deactivate_all_device(non_existent_id)

    # Then
    mock_notifier.assert_not_called()
