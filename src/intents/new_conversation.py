from src.domain.models.action_base import ActionBase
from src.domain.models.chat_message import ChatMessage


class NewConversation(ActionBase):
    action_name = "new_conversation"

    def __init__(self, emit, message: ChatMessage, session: dict):
        self.base = super().__init__(emit)
        self.message = message
        self.session = session

    def execute(self):
        message = "Hello! My name is Benny. I'm your friendly assistant. Ask me anything!"

        new_message = self.create_new_message(message, next_action="message_classifier")

        self.emit_message(new_message)