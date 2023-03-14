
import os
import random
import string
import json
import hashlib
from dotenv import load_dotenv
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
                                    

def verif_admin(mdp,user):
    load_dotenv(dotenv_path="admin")
    if user == os.getenv("USER") and hachage(mdp) == os.getenv("PASSWORD"):
        return True
    else:
        return False
    
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
    
def databaseMdp(mdp:str,user:str,message = []): #Pour mettre le fichier hasher dans un fichier
    dictmdp = {"mdp":mdp,"user":user,"message":message}     #On créer un dictionnaire, car le fichier est une liste de dictionnaire
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
                if verif_admin(mdp,user):
                    openUserWindow(True)
                else:
                    openUserWindow(False) #Si connexion, on lance un spaceinvader que j'ai fait à l'aide d'un tuto : pas de mérite mais du temps quand même :'( 
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
        passwords = ""
        for i in contenu["motdepasse"]:
            passwords += i["mdp"]
            passwords += "\n"
        showinfo("Les Mots De Passes",passwords)
    
fenetre = Tk()
fenetre.title("Accueuil")
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
        json.dump(jso, fichier,indent=4)
                
def voirUser():
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        usernames = ""
        for i in contenu["motdepasse"]:
            usernames += i["user"]
            usernames += "\n"
        showinfo("Les usernames",usernames)
def affichermdp():
    global lastuser
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        for i in contenu["motdepasse"]:
            if i["user"] == lastuser:
                showinfo("Votre Mot De Passe",i["mdp"])
         
def validemdp():
    mdp = newpassword.get()
    changemdp(mdp)
    newpassword.delete(0,END)

           
def changemdp(newMdp):
    global lastuser
    print(newMdp)
    listdico1 = []
    if verif_rules(newMdp) == True and verif_same(hachage(newMdp)) == True:
        with open("motdepasse.json","r") as fichier:
            contenu = json.load(fichier)
            for i in contenu["motdepasse"]:
                if i["user"] == lastuser:
                    listdico1.append({"mdp":hachage(newMdp),"user":lastuser,"message":i["message"]})
                else: 
                    listdico1.append(i)
        jso = {"motdepasse":listdico1}
        with open("motdepasse.json","w") as fichier:
            json.dump(jso, fichier,indent=4)
    else:
        return False

def userAdmin(olduser,newuser):
    global lastuser
    listdico1 = []
    if newuser != "" and verif_user(newuser) == True:
        with open("motdepasse.json","r") as fichier:
            contenu = json.load(fichier)
            for i in contenu["motdepasse"]:
                if i["user"] == olduser:
                    listdico1.append({"mdp":i["mdp"],"user":newuser,"message":i["message"]})
                else: 
                    listdico1.append(i)
        jso = {"motdepasse":listdico1}
        with open("motdepasse.json","w") as fichier:
            json.dump(jso, fichier,indent=4)
    else:
        return False 
def passwordAdmin(user,password):
    global lastuser
    listdico1 = []
    if verif_rules(password) and verif_same(hachage(password)) == True:
        with open("motdepasse.json","r") as fichier:
            contenu = json.load(fichier)
            for i in contenu["motdepasse"]:
                if i["user"] == user:
                    listdico1.append({"mdp":hachage(password),"user":user,'message':i["message"]})
                else: 
                    listdico1.append(i)
        jso = {"motdepasse":listdico1}
        with open("motdepasse.json","w") as fichier:
            json.dump(jso, fichier,indent=4)
    else:
        return False 
def suprAdmin(user,newuser):
    global lastuser
    listdico1 = []
    if user == newuser:
        with open("motdepasse.json","r") as fichier:
            contenu = json.load(fichier)
            for i in contenu["motdepasse"]:
                if i["user"] != user:
                    listdico1.append(i)
        jso = {"motdepasse":listdico1}
        with open("motdepasse.json","w") as fichier:
            json.dump(jso, fichier,indent=4)
    else:
        return False
def Envoiemessage(user,msg):
    global lastuser
    listdico1 = []
    if verif_user(user) == False:
        with open("motdepasse.json","r") as fichier:
            contenu = json.load(fichier)
            for i in contenu["motdepasse"]:
                if i["user"] == user:
                    newMessage = i["message"]
                    newMessage.append([str(msg),"Envoyé par {}".format(lastuser)])
                    listdico1.append({"mdp":i["mdp"],"user":user,'message': newMessage})
                else: 
                    listdico1.append(i)
        jso = {"motdepasse":listdico1}
        with open("motdepasse.json","w") as fichier:
            json.dump(jso, fichier,indent=4)
    else:
        return False
    
def suprmessage(user):
    listdico1 = []
    with open("motdepasse.json","r") as fichier:
            contenu = json.load(fichier)
            for i in contenu["motdepasse"]:
                if i["user"] == user:
                    listdico1.append({"mdp":i["mdp"],"user":user,'message': []})
                else: 
                    listdico1.append(i)
    jso = {"motdepasse":listdico1}
    with open("motdepasse.json","w") as fichier:
            json.dump(jso, fichier,indent=4)
def viewMessage():
    global lastuser
    with open("motdepasse.json","r") as fichier:
        contenu = json.load(fichier)
        for i in contenu["motdepasse"]:
            if i["user"] == lastuser:
                showinfo("Vos Messages",i["message"])
                suprmessage(lastuser)
#command bouton
def alert():
    showinfo("alerte", "Bravo!")
def jouer():
    os.system('SpaceInverd.py')
menubar = Menu(fenetre)

def openTest():
    global newpassword
    fenetreUser = Toplevel(fenetre,cursor="target")
    fenetreUser.title("New Window")
    fenetreUser.geometry("1080x720")
    fenetreUser.minsize(480,360)
    fenetreUser.config(background="black")
    newFrame = Frame(fenetreUser)
    newFrame.config(background="black")
    labelConnect = Label(newFrame,text="Nouveau Mot De Passe",background="black",fg="green",font=("Arial",25))
    labelConnect.pack()
    newpassword = Entry(newFrame)
    newpassword.config(background="black",fg="green")
    newpassword.pack()
    boutonGame=Button(newFrame, text="Accepter",  background="green",fg="white",command=lambda: [validemdp(), fenetreUser.destroy()])
    boutonGame.pack()
    menubar = Menu(fenetreUser)
    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="Supprimer son compte", command=supprimer)
    menu1.add_command(label="Voir son mot de passe", command=affichermdp)
    menu1.add_command(label="Changer son mot de passe", command=openTest)
    menubar.add_cascade(label="Connecté en tant que '{}'".format(lastuser), menu=menu1)
    newFrame.pack(expand=YES)
    fenetreUser.config(menu=menubar)
    
def openMessage():
    global newpassword
    fenetreUser = Toplevel(fenetre,cursor="target")
    fenetreUser.title("New Window")
    fenetreUser.geometry("1080x720")
    fenetreUser.minsize(480,360)
    fenetreUser.config(background="black")
    newFrame = Frame(fenetreUser)
    newFrame.config(background="black")
    labelUser = Label(newFrame,text="L'utilisateur",background="black",fg="green",font=("Arial",25))
    labelUser.pack()
    username = Entry(newFrame)
    username.pack()
    username.config(background="black",fg="green")
    labelNewUser = Label(newFrame,text="Envoyer un message",background="black",fg="green",font=("Arial",25))
    labelNewUser.pack()
    message = Entry(newFrame)
    message.config(background="black",fg="green")
    message.pack()
    boutonGame=Button(newFrame, text="Envoyer",  background="green",fg="white",command=lambda: [Envoiemessage(username.get(),message.get()), fenetreUser.destroy()])
    boutonGame.pack()
    newFrame.pack(expand=YES)
def openAdminUsername():
    global newpassword
    fenetreUser = Toplevel(fenetre,cursor="target")
    fenetreUser.title("New Window")
    fenetreUser.geometry("1080x720")
    fenetreUser.minsize(480,360)
    fenetreUser.config(background="black")
    newFrame = Frame(fenetreUser)
    newFrame.config(background="black")
    labelUser = Label(newFrame,text="L'utilisateur",background="black",fg="green",font=("Arial",25))
    labelUser.pack()
    olduser = Entry(newFrame)
    olduser.pack()
    olduser.config(background="black",fg="green")
    labelNewUser = Label(newFrame,text="Le nouveau nom d'utilisateur",background="black",fg="green",font=("Arial",25))
    labelNewUser.pack()
    newuser = Entry(newFrame)
    newuser.config(background="black",fg="green")
    newuser.pack()
    boutonGame=Button(newFrame, text="Accepter",  background="green",fg="white",command=lambda: [userAdmin(olduser.get(),newuser.get()), fenetreUser.destroy()])
    boutonGame.pack()
    newFrame.pack(expand=YES)
    
def openAdminPassword():
    global newpassword
    fenetreUser = Toplevel(fenetre,cursor="target")
    fenetreUser.title("New Window")
    fenetreUser.geometry("1080x720")
    fenetreUser.minsize(480,360)
    fenetreUser.config(background="black")
    newFrame = Frame(fenetreUser)
    newFrame.config(background="black")
    labelUser = Label(newFrame,text="L'utilisateur",background="black",fg="green",font=("Arial",25))
    labelUser.pack()
    olduser = Entry(newFrame)
    olduser.pack()
    olduser.config(background="black",fg="green")
    labelNewUser = Label(newFrame,text="Le nouveau mot de passe",background="black",fg="green",font=("Arial",25))
    labelNewUser.pack()
    newpass = Entry(newFrame)
    newpass.config(background="black",fg="green")
    newpass.pack()
    boutonGame=Button(newFrame, text="Accepter",  background="green",fg="white",command=lambda: [passwordAdmin(olduser.get(),newpass.get()), fenetreUser.destroy()])
    boutonGame.pack()
    newFrame.pack(expand=YES)
def openSuprAdmin():
    global newpassword
    fenetreUser = Toplevel(fenetre,cursor="target")
    fenetreUser.title("New Window")
    fenetreUser.geometry("1080x720")
    fenetreUser.minsize(480,360)
    fenetreUser.config(background="black")
    newFrame = Frame(fenetreUser)
    newFrame.config(background="black")
    labelUser = Label(newFrame,text="L'utilisateur",background="black",fg="green",font=("Arial",25))
    labelUser.pack()
    olduser = Entry(newFrame)
    olduser.pack()
    olduser.config(background="black",fg="green")
    labelNewUser = Label(newFrame,text="Confirmer l'utilisateur à supprimer",background="black",fg="green",font=("Arial",20))
    labelNewUser.pack()
    newuser = Entry(newFrame)
    newuser.config(background="black",fg="green")
    newuser.pack()
    boutonGame=Button(newFrame, text="Accepter",  background="green",fg="white",command=lambda: [suprAdmin(olduser.get(),newuser.get()), fenetreUser.destroy()])
    boutonGame.pack()
    newFrame.pack(expand=YES)
def openUserWindow(admin):
    fenetreUser = Toplevel(fenetre,cursor="target")
    fenetreUser.title("New Window")
    fenetreUser.geometry("1080x720")
    fenetreUser.minsize(480,360)
    fenetreUser.config(background="black")
    newFrame = Frame(fenetreUser)
    newFrame.config(background="black")
    labelConnect = Label(newFrame,text="Vous voilà connecté {}".format(lastuser,str(admin)),background="black",fg="green",font=("Arial",25))
    labelConnect.pack()
    boutonGame=Button(newFrame, text="Jouer",  background="green",fg="white",command=jouer)
    boutonGame.pack()
    if admin:
        labelAdmin = Label(newFrame,text="Vous Voilà Monsieur L'admin",background="black",fg="green",font=("Arial",15))
        labelAdmin.pack()
        menubar = Menu(fenetreUser)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Envoyer un message",command=openMessage)
        menu1.add_command(label="Voir ses messages",command=viewMessage)
        menu1.add_command(label="Changer un nom d'utilisateur", command=openAdminUsername)
        menu1.add_command(label="changer un mot de passe", command=openAdminPassword)
        menu1.add_command(label="Supprimer un compte", command=openSuprAdmin)
        menu1.add_command(label="Voir les users",command=voirUser)
        menubar.add_cascade(label="Connecté en tant que '{}' l'admin".format(lastuser), menu=menu1)
    else:
        menubar = Menu(fenetreUser)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Envoyer un message",command=openMessage)
        menu1.add_command(label="Voir ses messages",command=viewMessage)
        menu1.add_command(label="Supprimer son compte", command=supprimer)
        menu1.add_command(label="Voir son mot de passe", command=affichermdp)
        menu1.add_command(label="Changer son mot de passe", command=openTest)
        menubar.add_cascade(label="Connecté en tant que '{}'".format(lastuser), menu=menu1)
    newFrame.pack(expand=YES)
    fenetreUser.config(menu=menubar)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Afficher", command=afficher)
menubar.add_cascade(label="Mot de passe", menu=menu1)
fenetre.config(menu=menubar)
fenetre.mainloop()


