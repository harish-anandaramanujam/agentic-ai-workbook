import random

class HelloWorldAIAgent:
    def __init__(self, name):
        self.name = name
        self.greetings = ["Hello", "Hi", "Hey there", "Greetings"]

    def perceive(self):
        # Normally you'd get input from the world. We'll simulate it
        user_input = input("You: ")
        return user_input

    def decide(self, perception):
        # AI "decides" how to respond based on input
        if "hello" in perception.lower():
            action = random.choice(self.greetings)
        else:
            action = "I don't understand. Say hello!"
        return action

    def act(self, decision):
        print(self.name, decision)

    def run(self):
        while True:
            perception = self.perceive()
            decision = self.decide(perception)
            self.act(decision)

if __name__ == "__main__":
    agent = HelloWorldAIAgent("Aiden")
    agent.run()
