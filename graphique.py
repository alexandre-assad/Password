import random
import json
import hashlib
from tkinter import *
from tkinter.messagebox import *

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
    if verif_rules(mdp):
        if verif_same(hachage(mdp)):
            error.config(text="Le mot de passe est valable",fg="blue")
            mdp = hachage(mdp)
            databaseMdp(mdp)
        else:
            error.config(text="Ce mot de passe est déjà utilisé, veuillez en choisir un autre",fg="red")
            
    else:
        error.config(text="Veuillez choisir un mot de passe qui respecte les règles",fg="red")
        
    
    

def afficher():
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        motdepasses = ""
        for i in contenu.values():
            motdepasses += i[0]["mdp"]
            motdepasses += "\n"
        showinfo("Les mots de passes",contenu)
    
fenetre = Tk()
fenetre.geometry("1080x720")
fenetre.minsize(480,360)
frame = Frame(fenetre)
mdp = ""
def entrer():
    mdp = my_password.get()
    mot_de_passe(mdp)

labelUser=Label(frame,text="Nom d'Utilisateur",font=("Courrier",15))
labelUser.pack()
my_username = Entry(frame)
my_username.pack()
    
labelPassword=Label(frame,text="Mot de Passe",font=("Courrier",15))
labelPassword.pack()
#Bouton et input
my_password = Entry(frame)
my_password.pack()
bouton=Button(frame, text="Valider", command=entrer)
bouton.pack(side=TOP, padx=50, pady=10)
#Error
error=Label(frame,text="erreur",fg="white")
error.pack()
#frame
frame.pack(expand=YES)

#menu
def alert():
    showinfo("alerte", "Bravo!")

menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Afficher", command=afficher)
menubar.add_cascade(label="Mot de passe", menu=menu1)
fenetre.config(menu=menubar)
fenetre.mainloop()

