from src.domain.models.action_base import ActionBase
from src.domain.models.chat_message import ChatMessage
from src.domain.services.llms.openai import ask_llm_agent
from src.intents.ask_llm_intent import AskLLMIntent
from src.intents.rag_intent import RAGIntent


class MessageClassifierIntent(ActionBase):
    action_name = "message_classifier"

    def __init__(self, emit, message: ChatMessage, session: dict):
        self.base = super().__init__(emit)
        self.message = message
        self.session = session

    def execute(self):

        prompt = f"""Classify the following message into one of the following categories: 
        1. duplocloud
        2. other
        
        Any message that contains the word "duplocloud" or asks a question about CI/CD should be classified as "duplocloud". Else, it should be classified as "other". 
        
        Only answer with either "duplocloud" or "other".
        
        Message: {self.message.message}
    
        """


        llm_response = ask_llm_agent(ChatMessage.new_bot_message(prompt))

        # need to do an 'in', because LLM is return other text with the classification
        if 'duplocloud' in llm_response:
            RAGIntent(emit=self.emit, message=self.message, session=self.session).execute()
        else:
            AskLLMIntent(emit=self.emit, message=self.message, session=self.session).execute()
