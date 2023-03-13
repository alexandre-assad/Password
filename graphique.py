
import os
import random
import string
import json
import hashlib
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog as fd

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
                                    
       
def verif_same(mdp): #Pour vérifieir si le mot de passe existe déjà
    with open("motdepasse.json","r") as fichier: #On ouvre pour parcourir le fichier JSON
        contenu = json.load(fichier)
        for i in contenu["motdepasse"]:
            if i["mdp"] == mdp: #Si un mot de passe correspond à un présent dans le fichier, c'est False
                return False
        return True
                           
def hachage(str:str): #On va utiliser haslib pour hasher le mdp
    hach = hashlib.sha256(str.encode(encoding='utf-8')).hexdigest()
    return hach
            

def verif_user(user):  #Comme pour les mots de passes, on vérifie cette fois l'user
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        for i in contenu["motdepasse"]:
            if i["user"] == user:
                return False
        return True
    
def databaseMdp(mdp:str,user:str): #Pour mettre le fichier hasher dans un fichier
    dictmdp = {"mdp":mdp,"user":user}     #On créer un dictionnaire, car le fichier est une liste de dictionnaire
    with open ("motdepasse.json","r+") as fichier:
        donnees = json.load(fichier)
        donnees["motdepasse"].append(dictmdp)
        fichier.seek(0)
        json.dump(donnees,fichier,indent=4)


def connection(mdp,user): #Si le bon utilisateur a le bon mot de passe (un combiné de verif_user et verif_same)
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        for i in contenu["motdepasse"]:
            if i["user"] == user and i["mdp"] == mdp:
                return True
                
        return False
    
def mot_de_passe(mdp:str,user:str): #La ou on vérifie tous les impératifs du mot de passe et de l'username
    if verif_rules(mdp) == True and user != "":
        if connection(hachage(mdp),user):
                openNewWindow(user) #Si connexion, on lance un spaceinvader que j'ai fait à l'aide d'un tuto : pas de mérite mais du temps quand même :'( 
        elif verif_same(hachage(mdp)) == True and verif_user(user):
            error.config(text="Le mot de passe est valable",fg="blue") #On vérifie si la création du compte est possible
            mdp = hachage(mdp) #On hache le mdp et l'ajoute à la base de données
            databaseMdp(mdp,user)
        else:#Sinon c'est ERREUR
            error.config(text="Ce mot de passe ou ce nom d'utilisateur est déjà utilisé, veuillez en choisir un autre",fg="red")
            
    else:
        error.config(text="Veuillez choisir un mot de passe qui respecte les règles et bien renseigner votre username",fg="red")
        
    
    
#la fonction afficher, présent dans la menuBar de la fenetre
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
fenetre.config(background="black")
frame = Frame(fenetre)
frame.config(background="black")
mdp = ""
lastuser=""
def entrer():
    global lastuser
    user = my_username.get()
    lastuser = user
    mdp = my_password.get()
    mot_de_passe(mdp,user)
    my_password.delete(0,END)
    my_username.delete(0,END)

def generer():
    taille_min = 12
    taille_max = 18
    password = ""
    caracteres = string.ascii_letters + string.punctuation + string.digits  
    for i in range(random.randint(taille_min,taille_max)):
        password += "".join(random.choice(caracteres))
    my_password.delete(0,END)
    my_password.insert(0,password)

    
labelUser=Label(frame,text="Nom d'Utilisateur",font=("Courrier",15),background="black",fg="green")
labelUser.pack()
my_username = Entry(frame)
my_username.config(background="black",fg="green")
my_username.pack()
    
labelPassword=Label(frame,text="Mot de Passe",font=("Courrier",15),background="black",fg="green")
labelPassword.pack()
#Bouton et input
my_password = Entry(frame)
my_password.config(background="black",fg="green")
my_password.pack()
bouton=Button(frame, text="Valider",  background="green",fg="white",command=entrer)
bouton.pack(side=RIGHT, padx=50, pady=10)
boutonGenerer=Button(frame, text="Générer", background="green",fg="white",command=generer)
boutonGenerer.pack(side=LEFT, padx=50, pady=10)
#Error
error=Label(frame,text="erreur",fg="black",background="black")
error.pack()
#frame
frame.pack(expand=YES)

#supprimer
def supprimer():
    global lastuser
    listdico1 = []
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        for i in contenu["motdepasse"]:
            if i["user"] != lastuser:
                listdico1.append(i)
    jso = {"motdepasse":listdico1}
    with open("motdepasse.json","w") as fichier:
        json.dump(jso, fichier)
                

def affichermdp():
    global lastuser
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        for i in contenu["motdepasse"]:
            if i["user"] == lastuser:
                showinfo("Votre Mot De Passe",i["mdp"])
        
#command bouton
def alert():
    showinfo("alerte", "Bravo!")
def jouer():
    os.system('SpaceInverd.py')
menubar = Menu(fenetre)

def openNewWindow(user):
    fenetreUser = Toplevel(fenetre)
    fenetreUser.title("New Window")
    fenetreUser.geometry("1080x720")
    fenetreUser.minsize(480,360)
    fenetreUser.config(background="black")
    newFrame = Frame(fenetreUser)
    newFrame.config(background="black")
    labelConnect = Label(newFrame,text="Vous voilà connecté {}".format(user),background="black",fg="green",font=("Arial",25))
    labelConnect.pack()
    boutonGame=Button(newFrame, text="Jouer",  background="green",fg="white",command=jouer)
    boutonGame.pack()
    menubar = Menu(fenetreUser)
    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="Supprimer son compte", command=supprimer)
    menu1.add_command(label="Voir son mot de passe", command=affichermdp)
    menubar.add_cascade(label="Connecté", menu=menu1)
    newFrame.pack(expand=YES)
    fenetreUser.config(menu=menubar)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Afficher", command=afficher)
menubar.add_cascade(label="Mot de passe", menu=menu1)
fenetre.config(menu=menubar)
fenetre.mainloop()

