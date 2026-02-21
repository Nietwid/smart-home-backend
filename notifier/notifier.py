from notifier.message import NotifierMessage


class Notifier:
    def notify(self, messages: list[NotifierMessage]):
        for message in messages:
            print(message)


notifier = Notifier()