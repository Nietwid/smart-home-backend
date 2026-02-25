from dispatcher.command_message import CommandMessage
from dispatcher.dispatcher import action_event_dispatcher
from notifier.notifier import notifier


class ActionEventCommandProcessor:

    def __call__(self, message: CommandMessage) -> None:
        result = action_event_dispatcher.dispatch(message)
        notifier.notify(result.notifications)


action_event_command_processor = ActionEventCommandProcessor()
