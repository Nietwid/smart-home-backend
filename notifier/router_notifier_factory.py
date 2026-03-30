from typing import TYPE_CHECKING
from consumers.router.message.message import DeviceRouterMessage
from notifier.message import RouterNotifierData
if TYPE_CHECKING:
    from dispatcher.device.messages.device_message import DeviceMessage

class RouterNotifierFactory:

    def device_message(self,router_mac:str, message:"DeviceMessage")->"RouterNotifierData":
        return RouterNotifierData(
                router_mac=router_mac,
                data=DeviceRouterMessage(
                    payload= message
                )
            )


router_notifier_factory = RouterNotifierFactory()