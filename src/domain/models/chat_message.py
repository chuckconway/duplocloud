import json


class ChatMessage:
    purpose: str = ''
    message: str = ''
    options: list[str] = []
    sender: str = ''
    uuid: str = ''
    action_name: str = ''

    @staticmethod
    def new_bot_message(message: str):
        new_message = ChatMessage()
        new_message.message = message
        new_message.sender = 'bot'
        return new_message

    @staticmethod
    def load_from_dict(dictionary) -> 'ChatMessage':
        message = ChatMessage()
        message.purpose = dictionary.get('purpose', '')
        message.message = dictionary.get('message', '')
        message.options = dictionary.get('options', [])
        message.sender = dictionary.get('sender', '')
        message.uuid = dictionary.get('uuid', '')
        message.action_name = dictionary.get('actionName', '')

        return message