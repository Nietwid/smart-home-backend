from consumers.frontend.messages.messenger import frontend_messenger
from consumers.router.message.enum import RouterMessageType
from consumers.router.messenger import router_messenger
from notifier.enum import Destinations
from notifier.message import NotifierMessage, RouterNotifierData, FrontendNotifierData, MicroserviceNotifierData
from notifier.utils.handle_microservice_outbox import handle_microservice_outbox
from notifier.utils.handle_router_outbox import handle_router_outbox


class Notifier:
    def notify(self, messages: list[NotifierMessage]):
        for message in messages:
            match message.destination:
                case Destinations.ROUTER:
                    message: RouterNotifierData
                    if message.data.target != RouterMessageType.DEVICE:
                        router_messenger.send(message.router_mac, message.data)
                        continue
                    handle_router_outbox(message)
                case Destinations.FRONTEND:
                    message: FrontendNotifierData
                    frontend_messenger.send(message.home_id, message)
                case Destinations.MICROSERVICE:
                    message: MicroserviceNotifierData
                    handle_microservice_outbox(message)




notifier = Notifier()