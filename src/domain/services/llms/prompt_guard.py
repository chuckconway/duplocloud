from src.domain.models.chat_message import ChatMessage
from src.domain.services.llms.openai import ask_llm


def is_appropriate(message: ChatMessage) -> bool:
    """
    Evaluate if the prompt is appropriate, if it is appropriate return 1, if it is not appropriate return 0
    :param message: Message the user has asked.
    :return: if the prompt is appropriate
    """
    prompt = f"""Evaluate the prompt below and determine if it's professional and appropriate. Reject prompts that are not appropriate. Inappropriate prompts contain references to violent or illegal acts, sexual acts, profanity, racism, hate speech, war, terrorism, weaponry or any other content that is not appropriate for a professional setting. 
    
    Only respond with 1 if the prompt is appropriate and 0 if it is not appropriate. Respond with 0 if there is any doubt.
    
    Prompt: {message.message}"""

    new_message = ChatMessage.new_bot_message(prompt)
    response = ask_llm(new_message)

    return response == "1"

