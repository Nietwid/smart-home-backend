from pydantic import BaseModel, Field, ConfigDict

from consumers.device.messages.message import DeviceMessage
from consumers.frontend.messages.message import FrontendMessage
from notifier.enum import Destinations


class NotifierMessage(BaseModel):
    destination:Destinations

class DeviceNotifierData(NotifierMessage):
    destination:Destinations = Field(default=Destinations.DEVICE)
    router_mac:str
    data: DeviceMessage

class FrontendNotifierData(NotifierMessage):
    destination:Destinations = Field(default=Destinations.FRONTEND)
    home_id: int
    data: FrontendMessage
