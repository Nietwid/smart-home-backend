from consumers.frontend.messages.messenger import frontend_messenger
from consumers.router.messenger import router_messenger
from notifier.enum import Destinations
from notifier.message import NotifierMessage, RouterNotifierData, FrontendNotifierData


class Notifier:
    def notify(self, messages: list[NotifierMessage]):
        for message in messages:
            match message.destination:
                case Destinations.ROUTER:
                    message: RouterNotifierData
                    router_messenger.send(message.router_mac, message)
                case Destinations.FRONTEND:
                    message: FrontendNotifierData
                    frontend_messenger.send(message.home_id, message)


notifier = Notifier()