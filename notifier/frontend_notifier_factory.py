from consumers.frontend.messages.message import FrontendMessage
from consumers.frontend.messages.types import FrontendMessageType
from notifier.message import FrontendNotifierData


class FrontendNotifierFactory:
    def update_peripheral_state(self,home_id:int, state:dict)->FrontendNotifierData:
        return FrontendNotifierData(
                home_id=home_id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_PERIPHERAL_STATE,
                    data=state
                )
        )

    def update_peripheral_pending(self,home_id:int, pending:list[str])->FrontendNotifierData:
        return FrontendNotifierData(
                home_id=home_id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_PERIPHERAL_PENDING, data=pending
                ),
            )

frontend_notifier_factory = FrontendNotifierFactory()

