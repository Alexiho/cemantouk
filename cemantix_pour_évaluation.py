#Problème actuel: quand les deux mots sont trop loins ou trop proches cela peut prendre beaucoup de temps.

"""

PRINCIPE GENERAL:
il faut que l'on crée un cémantix afin que l'on puisse in fine évaluer notre agent ia
pour cela on va donc créer une liste de mots qui sera la liste des mots à deviner
on va la demander où la chercher qqpart poour qu'elle soit le plus aléatoire possible
ensuite on va prendre un élémeent de cette liste
on va en calculer l'embedding
pour chaque nouvel élément que l'on nous donne en entrée on va en calculer l'embedding 
puis la distance entre les deux mots qui va être le correspondant à la température dans cémantix

POUR LE CODE:
-On va coder une fonction qui prend deux mots en entrée et nous donne la distance entre les deux.
Cela va être notre fonction de distance : fdistance
-On va avoir notre liste de mots tests à atteindre. On crée une fonction qui pioche de manière aléatoire dans
cette liste : fobjectif

On verra plus tard pour rendre cela plus cohérent et faire une boucle for qui parcourt la liste des mots
objectifs. On le fera une fois le chatbot fini. 

Ainsi notre utilisateur va utiliser une fois fobjectif pour son mot à chercher et va ensuite utiliser 
fdistance pour avoir à chaque essai la distance avec le mot objectif.
On s'en fiche que nous connaissions le mort objectif ce qui compte c'est que l'IA ne le sache pas. 
"""

################################################################################################################
#   CODE DE LA FONCTION DE DISTANCE
################################################################################################################

#importations
from langchain_openai import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
import math

# charge le fichier .env
load_dotenv()

#on définit la méthode sur les embeddings
def get_embeddings_endpoint():
    """Get the Azure OpenAI endpoint, removing /openai/v1 suffix if present."""
    endpoint = os.getenv("AI_ENDPOINT", "")
    if endpoint.endswith("/openai/v1"):
        endpoint = endpoint.replace("/openai/v1", "")
    return endpoint

#fonction cosine de distance entre les embeddings
def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    dot_product = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    return dot_product / (mag_a * mag_b)

#On va coder une fonction qui prend deux mots en entrée et nous donne la distance entre les deux.
#elle nous retourne la distance entre les deux. On verra pour la rendre plus palpable peut être.
#Et savoir de où à où peut aller le score.
#Cela va être notre fonction de distance : fdistance
def fdistance(objectif,essai):
    #on crée notre outil d'embedding
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=get_embeddings_endpoint(),
        api_key=os.getenv("AI_API_KEY"),
        model=os.getenv("AI_EMBEDDING_MODEL", "text-embedding-3-large"),
        api_version="2024-02-01",
    )
    
    #on calcule l'embedding de objectif
    embeddingobjectif = embeddings.embed_query(objectif)

    #on calcule l'embedding de essai
    embeddingessai = embeddings.embed_query(essai)

    #on calcule leur distance
    distance = cosine_similarity(embeddingobjectif,embeddingessai)

    #On la renvoit avec les textes sur la signifiactions des différentes scores. 
    # signifiactions des différentes scores. 
    print("Similar meanings → High similarity scores (>0.8)" \
    "Different topics → Low similarity scores (<0.5)")
    #on renvoit la distance
    return distance

#Test
print("test sur fdistance")
print(fdistance('lion','lionceau'))
print(fdistance('lion','lionne'))
print(fdistance('lion','chat'))
#Trop long:
#print(fdistance('lion','lion'))

################################################################################################################
#   CODE DE LA GENERATION D'OBJECTIFS
################################################################################################################

#V2 de fobjectif : fobjectif2
#On demande un mot à chatgpt.

#Importations
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

#Pour charger le fichier environnement
load_dotenv()

def fobjectif2():
    #On récupère le modèle
    model = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY"),
    )

    # On lui demande un mot au hasard
    question= "give me a random french word, just one word no sentence with it"

    #On récupère la réponse
    response = model.invoke(question)

    #On sort la réponse
    return response.content

#Test V2
print("test sur fobjectif2")
print(fobjectif2())


#TEST FINAL
#Test
print("test sur tout")
objectif=fobjectif2()
print(objectif)
print(fdistance(objectif,'lionceau'))
print(fdistance(objectif,'lionne'))
print(fdistance(objectif,'chat'))