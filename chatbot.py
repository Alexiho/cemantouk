"""
Multi-Turn Conversation
Run: python 02-chat-models/code/01_multi_turn.py

🤖 Try asking GitHub Copilot Chat (https://github.com/features/copilot):
- "Why do we need to append AIMessage to the messages list after each response?"
- "How would I implement a loop to keep the conversation going with user input?"
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


def main():

    model = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY")
    )

    # Start with system message and first question
    messages = [
        SystemMessage(content="Tu es un expert de la langue française et des champs lexicaux. Ton objectif est de trouver un mot un partir de tentatives. A chaque tentative, on te diras si tu es proches ou loin avec une température. Essaye des mots d'abords au hasard puis affine")
    ]

    while messages[len(messages)-1].content != "100" : 
        response = model.invoke(messages)
        print(f"\n 🤓AI: {response.content}")
        messages.append(AIMessage(content=str(response.content)))
        message=input("score : ")
        messages.append(HumanMessage(content=message))
    print(len(messages))

    
if __name__ == "__main__":
    main()
