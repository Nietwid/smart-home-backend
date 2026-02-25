from dispatcher.command_message.factory import command_message_factory


def test_command_message_factory(device_message_device_connect, home):
    command_message = command_message_factory.resolve(
        device_message_device_connect, 1, "1234"
    )
    assert command_message.device.mac == device_message_device_connect.device_id
    assert command_message.peripheral is None
