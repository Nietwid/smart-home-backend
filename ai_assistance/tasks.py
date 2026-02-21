from celery import shared_task

from ai_assistance.ai_assistance import AiAssistance
from consumers.frontend.messages.message import FrontendMessage
from consumers.frontend.messages.types import (
    FrontendMessageType,
)
from consumers.frontend.messages.messenger import FrontendMessenger


@shared_task
def ai_test(user, prompt, reply_chanel):
    ai = AiAssistance.get_instance()
    ai.run(user, prompt, reply_chanel)
    replay_message = FrontendMessage(
        action=FrontendMessageType.AI_RESPONSE,
        status=200,
        data={"message": "end"},
    )
    FrontendMessenger().send_to_channel(reply_chanel, replay_message)
