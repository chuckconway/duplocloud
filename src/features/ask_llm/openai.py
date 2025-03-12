import os

from src.domain.models.chat_message import ChatMessage
from smolagents import OpenAIServerModel, CodeAgent, DuckDuckGoSearchTool


def ask_llm_agent(message: ChatMessage) -> str:
    prompt = f"""
    When answering the following question, site the source for the answer, and provide a link, when possible, to the source. Format your answer in JSON, with the following format:

    {{source_name": "The name of the source", "source_url": "https://example.com", "answer": "The answer"}}
    
    Question:
    {message.message}
    """

    model = OpenAIServerModel(
        model_id="gpt-4o",
        api_key=os.environ["OPENAI_API_KEY"],  # Switch to the API key for the server you're targeting.
    )
    agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)
    response = agent.run(prompt, max_steps=3)

    return \
    f"""{response['answer']}\n\n *source*: {response['source_name']} ({response['source_url']})"""

def ask_llm(message: ChatMessage) -> str:
    from openai import OpenAI
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": message.message
            }
        ]
    )

    response = completion.choices[0].message.content
    return response
