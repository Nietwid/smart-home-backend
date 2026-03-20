from consumers.frontend.messages.message import FrontendMessage
from consumers.frontend.messages.types import FrontendMessageType
from notifier.message import FrontendNotifierData


class FrontendNotifierFactory:

    def update_router(self, home_id:int, data:dict)->FrontendNotifierData:
        return FrontendNotifierData(
                home_id=home_id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_ROUTER,
                    data=data
                )
        )

    def update_room(self, home_id:int, data:dict)->FrontendNotifierData:
        return FrontendNotifierData(
                home_id=home_id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_ROOM,
                    data=data
                )
        )

    def update_device(self, home_id:int, data:dict)->FrontendNotifierData:
        return FrontendNotifierData(
                home_id=home_id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_DEVICE,
                    data=data
                )
        )

    def update_device_required_action(self, home_id:int, actions:list[str], device_id:int)->FrontendNotifierData:
        return FrontendNotifierData(
                home_id=home_id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_DEVICE_REQUIRED_ACTION,
                    data={
                        "actions":actions,
                        "device_id":device_id
                    }
                )
        )

    def update_peripheral_state(self, home_id:int, state:dict)->FrontendNotifierData:
        return FrontendNotifierData(
                home_id=home_id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_PERIPHERAL_STATE,
                    data=state
                )
        )


    def update_peripheral_pending(self, home_id:int, device_id:int, peripheral_id:int, pending:list[str])->FrontendNotifierData:
        return FrontendNotifierData(
                home_id=home_id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_PERIPHERAL_PENDING, data={
                        "pending":pending,
                        "device_id":device_id,
                        "peripheral_id":peripheral_id
                    }
                )
            )
    def update_device_pending(self,home_id:int, device_id:int, pending:list[str])->FrontendNotifierData:
        return FrontendNotifierData(
                home_id=home_id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_DEVICE_PENDING, data={
                        "pending":pending,
                        "device_id":device_id,
                    }
                )
            )
    def display_toaster(self, home_id:int, message:str)->FrontendNotifierData:
        return FrontendNotifierData(
            home_id=home_id,
            data=FrontendMessage(
                action=FrontendMessageType.DISPLAY_TOASTER, data={
                    "message":message
                }
            )
        )

frontend_notifier_factory = FrontendNotifierFactory()

