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

def transfoStrToList(phrase : str):
    """Prends en entrée une chaine de la forme "[(clé,value),...]"
    et renvoie la liste ["(clé,value)",...]"""
    result=[]
    indiceDebut=1 #On ne prend pas le premier "["
    for i in range (len(phrase)):
        if phrase[i]==")":
            result.append(phrase[indiceDebut:i+1])
            indiceDebut=i+2
    return(result)

def transfoListToDico(liste : list):
    """Prends en entrée une liste de la forme ["(clé,value)",...]
    et renvoie le dictionnaire {clé : value ...}"""
    dico={}
    for couple in liste:
        for i in range(len(couple)):
            if couple[i]==",":
                clé=couple[1:i]
                valeur=couple[i+1:-1]
        try :
            dico[clé]=float(valeur)
        except TypeError:
            print("Type mismatch")
    return(dico)

def transfoStrToDico(phrase : str):
    """Prends en entrée une chaine de la forme [(clé,value),...]
    et renvoie le dictionnaire {clé : value ...}"""
    return(transfoListToDico(transfoStrToList(phrase)))


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

    messageSystem2 = SystemMessage(content="On va te donner des phrases qui contiennent chacune un mot à isoler, une proposition de réponse à un jeu. Tu ne dois renvoyer que ce mot.")

    model3 = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY")
    )

    message3 = [
        SystemMessage(content="On va te donner une liste de mots avec un score associé. Tu dois renvoyer uniquement une liste qui contient des couples (mots,score) sous la forme [(mot1,score1),(mot2,score2)...].")
    ]

    # Start with system message and first question
    messageSystem1 = SystemMessage(content="Tu es un expert de la langue française et des champs lexicaux. Ton objectif est de trouver un mot un partir d'un dictionnaire de mots avec un score d'adjacence sémantique ou contextuelle. Si le dictionnaire est vide ou n'a que des scores inférieurs à 20, tu essaiera des mots loins de tout ceux déjà proposés. Reste sur des mots non conjugués du dictionnaire Français.")

    init=input("Mots dont on dispose déjà : ")
    message3.append(HumanMessage(content=init))
    motsDejaConnus=model3.invoke(message3)
    dicoMotsConnus=transfoStrToDico(motsDejaConnus.content)
    best_score=-100
    while best_score != "100" :
        messages=[messageSystem1,HumanMessage(content=str(dicoMotsConnus))] 
        response = model.invoke(messages)
        print(f"\n 🤓AI: {response.content}")
        valeurEssai=input("score : ")
        try:
            nouveauMot=model2.invoke([messageSystem2,response.content]).content
            valeurNouveauMot=float(valeurEssai)
            if valeurNouveauMot>=best_score:
                best_score=valeurNouveauMot
            dicoMotsConnus[nouveauMot]=valeurNouveauMot
            if valeurEssai=="3.141592":
                messages=HumanMessage(content="Quelle est la réponse au cémantix d'aujourd'hui ?")
                response=model.invoke(messages)
                print(f"\n 🤓AI: {response.content}")
                print("test")
        except ValueError:
            print("Erreur de notation")
    print(len(messages))

    
if __name__ == "__main__":
    main()
