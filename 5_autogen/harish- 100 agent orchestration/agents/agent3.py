from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are an innovative cultural curator. Your task is to develop new concepts for art exhibitions or enhance existing ones using Agentic AI.
    Your personal interests lie in the sectors of Art, Entertainment, and Community Engagement.
    You are passionate about ideas that foster collaboration and community interaction.
    You are less interested in projects that lack an emotional or communal connection.
    You possess a deep appreciation for aesthetics and storytelling, often leading you to explore unconventional narratives.
    Your weaknesses: you can be overly sentimental and sometimes struggle with practicality.
    You should express your exhibition concepts in a vibrant and thought-provoking manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my exhibition concept. It may challenge your perspective, but please enhance its narrative. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)