from dispatcher.context.device_context import PeripheralsContext, DeviceContext
from dispatcher.enums import Scope
from typing import Protocol
from device.repository.device_repository import DeviceRepository, device_repository
from dispatcher.messages.device_message import DeviceMessage
from dispatcher.messages.frontend_message import FrontendActionMessage
from peripherals.repository import PeripheralRepository, peripheral_repository


class ContextBuilderMessage(Protocol):
    scope: Scope
    device_id: int | str
    peripheral_id: int


class ContextBuilder:

    def __init__(
        self, device_repo: DeviceRepository, peripheral_repo: PeripheralRepository
    ):
        self.device_repo = device_repo
        self.peripheral_repo = peripheral_repo

    def build(self, message: ContextBuilderMessage, home_id: int, router_mac: str):

        if message.scope == Scope.CPU:
            if isinstance(message, DeviceMessage):
                device = self.device_repo.get_by_mac(message.device_id)
            elif isinstance(message, FrontendActionMessage):
                device = self.device_repo.get_by_id(message.device_id)
            else:
                raise ValueError(
                    f"Unsupported device id type: {type(message.device_id), message.device_id}"
                )
            return DeviceContext(home_id=home_id, router_mac=router_mac, device=device)

        if message.scope == Scope.PERIPHERAL:
            peripheral = self.peripheral_repo.get_by_id_with_device(
                message.peripheral_id
            )
            return PeripheralsContext(
                home_id=home_id,
                router_mac=router_mac,
                peripheral=peripheral,
            )

        raise ValueError(f"Unsupported scope: {message.scope}")


context_builder = ContextBuilder(device_repository, peripheral_repository)
