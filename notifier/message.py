from pydantic import BaseModel, Field

from consumers.frontend.messages.message import FrontendMessage
from consumers.router.message.message import RouterMessage
from notifier.enum import Destinations


class NotifierMessage(BaseModel):
    destination:Destinations

class RouterNotifierData(NotifierMessage):
    destination:Destinations = Field(default=Destinations.ROUTER)
    router_mac:str
    data: RouterMessage

class FrontendNotifierData(NotifierMessage):
    destination:Destinations = Field(default=Destinations.FRONTEND)
    home_id: int
    data: FrontendMessage
