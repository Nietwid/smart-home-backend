from consumers.router_message.message_type import MessageType
from device.repository.device_repository import DeviceRepository
from hardware.device.device import DeviceHardware
from hardware.registry import HARDWARE_REGISTRY
from consumers.router_message.device_message import DeviceMessage


def process_device_message(message: DeviceMessage):
    """
    Routes and executes hardware-specific logic based on the incoming message type.

    This function acts as a dispatcher. It identifies the target device, determines
    whether the event concerns the main controller or a peripheral, and executes
    the corresponding handler from the registry.

    Args:
        message (DeviceMessage): A validated Pydantic model

    Returns:
        None

    Notes:
        - If 'peripheral_id' is 0, the function uses the global 'DeviceHardware' handler.
        - For other IDs, it lookups the handler in 'HARDWARE_REGISTRY' using the
          peripheral's name stored in the database.
        - Supports two communication patterns: REQUEST (inbound commands)
          and RESPONSE (outbound action confirmations).
    """
    device = DeviceRepository.get_device_with_peripheral_by_mac(
        message.device_id, message.peripheral_id
    )

    if not device:
        # TODO Log this event if the device is unknown
        return

    # Determine the correct handler strategy
    if message.peripheral_id == 0:
        handler = DeviceHardware
    else:
        peripheral = device.peripherals.first()
        handler = HARDWARE_REGISTRY[peripheral.name]

    # Execute the mapped function
    if message.message_type == MessageType.REQUEST.value:
        handler.events.get(message.message_event)(message, device)
    elif message.message_type == MessageType.RESPONSE.value:
        handler.actions.get(message.message_event)(message, device)
