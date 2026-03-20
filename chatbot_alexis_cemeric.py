# 1. Import required modules
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from cemantix_pour_evaluation import *


# 2. Load environment variables
load_dotenv()


def main():

    objectif=fobjectif2()
    print(f"Objectif à trouver : {objectif}")

    historique_essais = {}

    with open("system_msg.txt", "r", encoding="utf-8") as f:
        contenu = f.read()

    print(contenu[:100])

    # Create a chat model instance
    model = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY")
    )

    # Start with system message and first question
    messages = [
        #SystemMessage(content="You are a helpful coding tutor who gives clear, concise explanations."),
        SystemMessage(content=contenu),
    ]

    dernier_message = "maison"
    
    message_utilisateur = ""

    # Trier les mots du plus chaud au plus froid
    #classement = sorted(historique_essais.items(), key=lambda x: x[1], reverse=True)
    listScores=[]
    while(message_utilisateur != "quit" or historique_trié[0]!=1):
        print(f"Test du mot : {dernier_message}")
        score = fdistance(objectif, dernier_message)
        listScores.append(score)
        print(f"Score reçu : {score}")

        # First exchange
        message_utilisateur = input("You :")
        #messages.append(HumanMessage(content=dernier_message))
        response1 = model.invoke(messages)
        print(f"\nAI: {response1.content}")
        dernier_message = response1.content

        historique_essais[response1.content] = score

        historique_trié = sorted(historique_essais.items(), key=lambda x: x[1], reverse=True)
        messages = [
            SystemMessage(content=contenu),
            HumanMessage(content=str(historique_trié)) # on trie le dictionnaire des essais du plus chaud au plus froid
        ]
        #print(str(historique_essais))
        print(str(sorted(historique_essais.items(), key=lambda x: x[1], reverse=True)))
       

    print(f"📊 Total messages in history: {len(messages)} messages, that include 1 system message, 3 Human messages and 2 AI responses")
    plt.plot(listScores)
    plt.show()

if __name__ == "__main__":
    main()
