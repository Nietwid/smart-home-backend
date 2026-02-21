from pydantic import BaseModel

from consumers.frontend_message.frontend_message import FrontendMessage
from device_consumer.device_message import DeviceMessage
from notifier.enum import Destinations


class NotifierMessage(BaseModel):
    destination:Destinations

class DeviceNotifierData(NotifierMessage):
    router_mac:str
    data:DeviceMessage

class FrontendNotifierData(NotifierMessage):
    router_mac:str
    data:FrontendMessage
