from src.domain.models.action_base import ActionBase
from src.domain.models.chat_message import ChatMessage
from src.features.ask_llm.openai import ask_llm, ask_llm_agent


class AskLLMIntent(ActionBase):

    action_name = "ask_llm_intent"

    def __init__(self, emit, message: ChatMessage, session: dict):
        self.base = super().__init__(emit)
        self.message = message
        self.session = session

    def execute(self):

        llm_response = ask_llm_agent(self.message)

        new_message = self.create_new_message(llm_response, next_action="ask_llm_intent")

        self.emit_message(new_message)