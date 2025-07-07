# 🤖 Hello World AI Agent

This project is a **basic Goal-Oriented AI Agent** designed to demonstrate the fundamentals of building an AI agent system.  
It showcases how to:

✅ **Give it goals**  
✅ **Let it make decisions based on simple reasoning** (or easily extend it to ML)  
✅ **Interact with a simple environment**

---

## 📜 Overview

The **Hello World AI Agent** is a simple console-based agent that:

- **Perceives**: Reads user input from the environment (console).
- **Decides**: Uses basic reasoning (keyword matching and random greetings) to decide how to respond.
- **Acts**: Outputs a message to the console.
- **Loops**: Continuously interacts until the user exits.

---

## 🛠️ How It Works

1. **Goal**  
   The agent is initialized with a clear goal:  
   ➔ *"Respond to greetings appropriately."*

2. **Perceive**  
   The agent listens for input from the user via the console.

3. **Decide**  
   - If the user greets the agent (e.g., "hello", "hi"), the agent responds with a friendly greeting.
   - If the user says something else, the agent prompts them to greet it.

4. **Act**  
   The agent prints its response back to the console.

5. **Loop**  
   The interaction continues until the user types `exit`, `quit`, or `bye`.

---

## 📂 Files

- `agent.py` — Main agent code.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/harish-anandaramanujam/ai-agents.git
cd hello-world-agent
```


### 2. Run the Agent

```bash
python agent.py
```

## 🧠 Future Improvements

- Integrate a simple ML model (e.g., text classification) to detect more complex intents.
- Extend the environment to include multiple agent types or richer interactions.
- Add memory to allow the agent to "remember" past conversations.
