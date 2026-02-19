from typing import Optional

from pydantic import BaseModel
from device.models import Device
from peripherals.models import Peripherals


class BaseContext(BaseModel):
    home_id: int
    router_mac: str

    class Config:
        arbitrary_types_allowed = True


class DeviceContext(BaseContext):
    device: Optional[Device]


class PeripheralsContext(BaseContext):
    peripheral: Peripherals
