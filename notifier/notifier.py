from consumers.frontend.messages.messenger import frontend_messenger
from consumers.router.messenger import router_messenger
from notifier.enum import Destinations
from notifier.message import NotifierMessage, RouterNotifierData, FrontendNotifierData, MicroserviceNotifierData
from notifier.tasks import send_microservice_notification


class Notifier:
    def notify(self, messages: list[NotifierMessage]):
        for message in messages:
            match message.destination:
                case Destinations.ROUTER:
                    message: RouterNotifierData
                    router_messenger.send(message.router_mac, message.data)
                case Destinations.FRONTEND:
                    message: FrontendNotifierData
                    frontend_messenger.send(message.home_id, message)
                case Destinations.MICROSERVICE:
                    message: MicroserviceNotifierData
                    send_microservice_notification.apply_async(args=(message.data.model_dump(),),queue=message.queue_name.value)

notifier = Notifier()