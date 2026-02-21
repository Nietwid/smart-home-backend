from consumers.frontend.messages.message import FrontendMessage
from consumers.frontend.messages.types import FrontendMessageType


class FrontendMessageBuilder:

    def build(self,action:FrontendMessageType, data:dict, status=200)-> FrontendMessage:
        return FrontendMessage(
            action= action ,
            status = status,
            data = data,
        )



frontend_message_builder = FrontendMessageBuilder()