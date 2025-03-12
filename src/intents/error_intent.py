from src.domain.models.action_base import ActionBase
from src.domain.models.chat_message import ChatMessage
from src.intents.new_conversation import NewConversation


class ErrorAction(ActionBase):

    action_name = "error_action"

    def __init__(self, emit, message: ChatMessage, session: dict):
        self.base = super().__init__(emit)
        self.message = message
        self.session = session

    def execute(self):
        message = "Oh no! I'm sorry, but I didn't understand your request. Let's start over!"

        print(message)

        new_message = self.create_new_message(message, "error_action")

        self.emit_message(new_message)

        NewConversation(emit=self.emit, message=self.message, session=self.session).execute()