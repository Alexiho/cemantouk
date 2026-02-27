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

    model2 = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY")
    )

    message2 = [
        SystemMessage(content="On va te donner des phrases qui contiennent chacune un mot à isoler, une proposition de réponse à un jeu. Tu ne dois renvoyer que ce mot.")
    ]

    # Start with system message and first question
    messages = [
        SystemMessage(content="Tu es un expert de la langue française et des champs lexicaux. Ton objectif est de trouver un mot un partir de tentatives. A chaque tentative, on te diras si tu es proches ou loin avec une température (max 100°C, évolution logarithmique). Essaye des mots d'abords au hasard jusqu'à avoir plusieurs scores de plus de 50, puis affine. Tu commencera en proposant un premier mot. Il t'es interdit de dire plusieurs fois le même mot")
    ]
    init=input("Mots dont on dispose déjà : ")
    init="Mots dont on connait déjà la température : " + init
    messages.append(HumanMessage(content=init))
    best_score=-100
    best_world=""
    while messages[len(messages)-1].content != "100" : 
        response = model.invoke(messages)
        print(f"\n 🤓AI: {response.content}")
        messages.append(AIMessage(content=str(response.content)))
        message=input("score : ")
        messages.append(HumanMessage(content=message))
        try:
            if message=="inconnu":
                messages.append(SystemMessage(content="Reste sur des mots non conjugués du dictionnaire Français."))
            elif float(message)>best_score:
                best_score=float(message)
                message2.append(HumanMessage(content=response.content))
                best_world=model2.invoke(message2).content
                message2.remove(HumanMessage(content=response.content))
            if best_score<15:
                messages.append(SystemMessage(content="Change de champ lexical."))
            elif float(message)<15:
                messages.append(SystemMessage(content=f"Rapproche toi de {best_world}"))
            messages.append(HumanMessage(content=f"Le meilleur mot est {best_world} avec {best_score}"))
            print(f"Le meilleur mot est {best_world} avec {best_score}")
        except ValueError:
            print("Erreur de notation")
    print(len(messages))

    
if __name__ == "__main__":
    main()
