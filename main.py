import random
import json
import hashlib
from tkinter import *


def verif_rules(str): #On va vérifier si le mot de passe est possible
    verification = False
    if len(str) >= 8:
        for i in str:
            if i.isupper():
                for i in str:
                    if i.islower():
                        for i in str:
                            if i.isnumeric():
                                for i in str:
                                    if i.isalpha() == False and i.isnumeric() == False:
                                        verification = True
    return verification
                                    
       
def verif_same(mdp):
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        for i in contenu["motdepasse"]:
            if i["mdp"] == mdp:
                return False
        return True
                           
def hachage(str:str): #On va utiliser haslib pour hasher le mdp
    hach = hashlib.sha256(str.encode(encoding='utf-8')).hexdigest()
    return hach
            
    
def databaseMdp(mdp:str): #Pour mettre le fichier hasher dans un fichier
    dictmdp = {"mdp":mdp}
    with open ("motdepasse.json","r+") as fichier:
        donnees = json.load(fichier)
        donnees["motdepasse"].append(dictmdp)
        fichier.seek(0)
        json.dump(donnees,fichier,indent=4)


def mot_de_passe(mdp:str):
    verification = False
    while verification is False:
        if verif_rules(mdp):
            if verif_same(hachage(mdp)):
                verification = True
            else:
                mot_de_passe(str(input("Ce mot de passe est déjà utilisé, veuillez en choisir un autre\n")))
                verification=True
        else:
            mot_de_passe(str(input("Veuillez choisir un mot de passe qui respecte les règles\n")))
            verification = True
    mdp = hachage(mdp)
    databaseMdp(mdp)

def afficher():
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        return contenu
    
while True:
    action = int(input("""Que voulez vous faire :
    (1) Taper un mot de passe
    (2) Voir les mots de passes
    (3) Sortir du programme
    """))
    if action == 1:
        mot_de_passe(str(input("Veuillez choisir un mot de passe qui respecte les règles\n")))
    elif action == 2:
        print(afficher())
    elif action == 3:
        break

