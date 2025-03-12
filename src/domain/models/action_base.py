import orjson

from src.domain.models.chat_message import ChatMessage


class ActionBase:
    def __init__(self, emit):
        self.emit = emit

    @staticmethod
    def create_new_message(message: str, next_action: str):
        chat_message = ChatMessage.new_bot_message(message)
        chat_message.action_name = next_action
        return chat_message

    def emit_message(self, message):
        serialized_data = orjson.dumps(message.__dict__)
        self.emit('message', serialized_data, broadcast=False)