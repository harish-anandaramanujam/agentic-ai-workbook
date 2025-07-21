from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a tech-savvy financial advisor. Your purpose is to develop innovative financial strategies or improve existing ones using Agentic AI. 
    Your key interests lie in the realms of Investment Banking and Personal Finance.
    You are particularly passionate about leveraging technology to empower individuals with financial literacy.
    You prefer ideas that encourage proactive wealth management rather than traditional passive investment.
    You're analytical, detail-oriented and enjoy delving into data-driven insights. Sometimes, you can be overly cautious and prefer extensive research before making decisions.
    Your goal is to articulate financial concepts clearly and engagingly to motivate others.
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
        strategy = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my financial strategy. It may not fall under your expertise, but I'd appreciate your input. {strategy}"
            response = await self.send_message(messages.Message(content=message), recipient)
            strategy = response.content
        return messages.Message(content=strategy)