# -*- coding: utf-8 -*-
"""
Created on Sun May 28 16:31:43 2023

@author: DIALLO_LEY
"""

#import os
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
import sqlite3
from random import shuffle, choice
import PIL
#import for icon making

import tkinter as tk
from PIL import Image, ImageTk
   
root = Tk()
root.title("TIRAGE AU SORT | COORDINATION DES ETUDIANTS DE L'UAM")
#image = Image.open("uam_400x400.jpg")
root.iconbitmap("uam_400x400_black_white.ico")

#icone=PhotoImage(file='C:\\UAM\\2023_Projects-2023\\Tournoi_UAM\\uam_400x400.jpg')
#root.iconphoto(False, icone)
#root.iconbitmap('C:\\UAM\\2023_Projects-2023\\Tournoi_UAM\\uam_400x400.png')

#img = PhotoImage(file='C:\\UAM\\2023_Projects-2023\\Tournoi_UAM\\uam_400x400.ico')
#img = ImageTk.PhotoImage(Image.open("uam_400x400.jpg"))  # PIL solution
#root.photoicon(False, img)

root.geometry("1250x600")
#root.resizable(0,0)
#root.attributes('-fullscreen', True)


# Titre
Titre = Label(root , text = "COUPE Du PATRIARCHE" , #foreground
              font = ("broadway 22 bold") , bg="#AE5D2D" , fg = "lightblue" )
Titre.grid(row = 0, column = 0)

#cette variable nous permettra de limiter le nombre d'execution d'une scope
#   (une partie du programme)
initial_exe = 0 
# Nous initialisons une variable pour le tirage au sort
# elle nous permettra de de controler le nombre de match à effectuer
cpt = 0
global nbre_equipe #variable globale determinant le nbre d'equipes dans la bd
class Tournoi:
    
    def __init__(self, master):
        pass
        

    def Ajout_Equipe(self):
        """
        NOM_equipe = entreeEquipe.get()
        
        if NOM_equipe =="" :
            mb.showerror('Error!', "SORRY, le nom d'équipe saisie est invalide...")
        """
        NOM_equipe = Tournoi.validation_ajout(self)
        if NOM_equipe != None:
            # Connection pour l'Affichage sur sqlite
            connection = sqlite3.connect("equipes.db")
            curseur = connection.cursor()
            curseur.execute("INSERT INTO EQUIPE (`Nom_Equipe`) values (?)",
                        (NOM_equipe,)), connection.commit()
            connection.close()
        
            # Affichage auto sur Treeview
            connection = sqlite3.connect("equipes.db")
            curseur = connection.cursor()
            select = curseur.execute("SELECT Nom_Equipe FROM EQUIPE order by id desc")
            #select = curseur.execute("SELECT*FROM EQUIPE")
            select = list(select)
            Affiche.insert("", END, values = select[0])
            connection.close()
            
            """
            # Message de validation
            mb.showinfo("Enregistrement d'equipe",
                        "Votre EQUIPE a été ajoutée avec succès ! ")
            """
            
            # Nettoiement des entrees apres ajout:
            entreeEquipe.delete(0, END)
    
    
    """
    def insertion_tirage(self):
        connection = sqlite3.connect("tirage_results.db")
        curseur = connection.cursor()
        curseur.execute("INSERT INTO TIRAGE (`Nom_Equipe`) values (?)",
                    (NOM_equipe,)), connection.commit()
        connection.close()
    """
    
    
    def validation_ajout(self):
        # Nous recuperons la liste des equipes pour empecher le doublons d'équipe
        liste_equipe = Tournoi.liste_equipe(self)
        try:
            NOM_equipe = entreeEquipe.get()
            assert NOM_equipe != "" and NOM_equipe not in liste_equipe
            return NOM_equipe
            
        except AssertionError:
            mb.showerror('Error!', "Veuillez vous assurer que le nom d'équipe saisie est non vide OU qu'il n'existe pas déjà dans la liste des équipes. (La liste des équipes ne peut contenir de doublon)...")   
            return None
        
    
    def nouveau_tirage(self):
        global initial_exe
        initial_exe=0
        # On nettoie l'objet treeview pour le prochain tirage
        for equipes_tire in Affiche2.get_children():
             Affiche2.delete(equipes_tire)
             
        #On supprime les elt de la BD EQUIPE et on nettoie le treeview
        Tournoi.Supprimer_tout(self)
    
    
    def Supprimer_equipe(self):
        idSelect = Affiche.item(Affiche.selection())['values'][0]
        #print(idSelect)
        conn = sqlite3.connect("equipes.db")
        cur = conn.cursor()
        #delete = cur.execute("delete from EQUIPE WHERE Nom_Equipe = {}".format(idSelect))
        delete = cur.execute("delete from EQUIPE WHERE Nom_Equipe = ?", (idSelect,))
        conn.commit()
        Affiche.delete(Affiche.selection())
        
    
    def Supprimer_tout(self):
        conn = sqlite3.connect("equipes.db")
        cur = conn.cursor()
        delete = cur.execute("DELETE FROM EQUIPE ")
        for item in Affiche.get_children():
            Affiche.delete(item)
        conn.commit()
        conn.close()
        
        
    def melanger(self):
        """
        conn = sqlite3.connect("equipes.db")
        cur = conn.cursor()
        #equipe = cur.execute("SELECT Nom_Equipe FROM EQUIPE")
        equipes = []
        for row in conn.execute("SELECT Nom_Equipe FROM EQUIPE"): 
            equipe = row[0];
            equipes.append(equipe)
        # On mélange à présent les equipes
        print(equipes)
        global equipes_aleatoire
        equipes_aleatoire = equipes[:]
        """
        global initial_exe
        if initial_exe == 0:
            #Cette execution nous permet aux variables globales de récupérer 
            #   leurs valeurs
            global nbre_equipe_value
            nbre_equipe_value = Tournoi.nbre_equipe(self)
            initial_exe += 1
        """
        print("dans melange : \n", equipes)
        print("----------- shuffle-----------------")
        """
        shuffle(equipes_aleatoire) # on mélange la liste des equipe
        #nettoiement du treeview:
        for i in Affiche.get_children():
             Affiche.delete(i)
        #insertion des nouvelles donnees melangees
        for row in equipes_aleatoire:
            Affiche.insert("", END, values = row)
            #print(row)
        
    
    def liste_equipe(self):
        conn = sqlite3.connect("equipes.db")
        cur = conn.cursor()
        #equipe = cur.execute("SELECT Nom_Equipe FROM EQUIPE")
        global liste_equipes
        liste_equipes = []
        for row in conn.execute("SELECT Nom_Equipe FROM EQUIPE"): 
            equipe = row[0];
            liste_equipes.append(equipe)
        conn.close()
        return liste_equipes
    
    
    def nbre_equipe(self):
        conn = sqlite3.connect("equipes.db")
        cur = conn.cursor()
        #equipe = cur.execute("SELECT Nom_Equipe FROM EQUIPE")
        global equipes
        equipes = []
        for row in conn.execute("SELECT Nom_Equipe FROM EQUIPE"): 
            equipe = row[0];
            equipes.append(equipe)
        conn.close()
        # On mélange à présent les equipes
        #print(equipes)
        global equipes_aleatoire
        equipes_aleatoire = equipes[:]
        #print("dans nbre_equipe()\n",equipes_aleatoire)
        return len(equipes)
    
        
    def tirer(self):
        #raise
        global initial_exe
        if initial_exe == 0:
            global nbre_equipe_value
            nbre_equipe_value = Tournoi.nbre_equipe(self)
            initial_exe += 1
        # compteur du nombre de tirage
        global cpt
        choix1 = choice(equipes_aleatoire)
        equipes_aleatoire.remove(choix1)
        cpt += 1
        #print(choix, cpt)
        
        if (nbre_equipe_value % 2 == 0): 
            choix2 = choice(equipes_aleatoire)
            equipes_aleatoire.remove(choix2)
            cpt += 1
            Affiche2.insert(parent='', index='end', text="",
                                values=((choix1, "vs", choix2)))
            # On retire les equipes tirés da la liste des équipes
            #nettoiement du treeview:
            for i in Affiche.get_children():
                 Affiche.delete(i)
            for row in equipes_aleatoire:
                Affiche.insert("", END, values = row)
            """
            for i in Affiche.get_children():
                if i == choix1 or i == choix2 :
                    Affiche.delete(i)
            """
            
            
            """
            if (cpt <= (nbre_equipe_value / 2)):
                Affiche2.insert(parent='', index='end', text="",
                                values=((choix1, "VS", choix2)))
            else:
                Affiche2.insert(parent='', index='end', text="",
                                values=((choix1,"VS", choix2)))
            """
        else:
            if (cpt < nbre_equipe_value): 
                choix2 = choice(equipes_aleatoire)
                cpt += 1
                equipes_aleatoire.remove(choix2)
                Affiche2.insert(parent='', index='end', text="",
                                    values=((choix1, "vs", choix2)))
                # On retire les equipes tirés da la liste des équipes
                #nettoiement du treeview:
                for i in Affiche.get_children():
                     Affiche.delete(i)
                for row in equipes_aleatoire:
                    Affiche.insert("", END, values = row)
                """
                for i in Affiche.get_children():
                    if i == choix1 or i == choix2 :
                        Affiche.delete(i)
                """
                
            else:
                Affiche2.insert(parent='', index='end', text="",
                                    values=((choix1, "(QUALIF.)")))
                # On retire les equipes tirés da la liste des équipes
                #nettoiement du treeview:
                for i in Affiche.get_children():
                     Affiche.delete(i)
                for row in equipes_aleatoire:
                    Affiche.insert("", END, values = row)
                
                """
                for i in Affiche.get_children():
                    if i == choix1 or i == choix2 :
                        Affiche.delete(i)
                """
        
        
        """
        connection = sqlite3.connect("tirage_results.db")
        curseur = connection.cursor()
        select = curseur.execute("SELECT * FROM TIRAGE")
        for record in select:
            Affiche2.insert(parent='', index='end', text="",
                         values=(record[0], record[1], record[2], record[3]))

        connection.close()
        """
        
    
    def Aide(self):
        mb.showinfo("Assistant Général",
                    "Pour effectuer un nouveau TIRAGE, veuillez clicquez sur NOUVEAU TIRAGE...")
        mb.showinfo("Assistant Général",
                    "Ensuite Veuillez renseigner les différentes équipes (sans Doublon), Vous pouvez Melanger les équipes avant d\'effectuer un Tirage si vous le désirez !")
        mb.showinfo("Assistant Général",
                    "En cas d'erreur de saisie, Aidez-vous des Boutons SUPPRIMER SELECTION pour supprimer l\'équipe sélectionnée Ou encore SUPPRIMER TOUT pour reprendre à 0 la saisie. A la fin du Tirage, Veuillez noter les résultats (ils ne seront pas gardés)...")
        
    
    def Quiter(self):
        root.destroy()
        

T = Tournoi(root)


# Configuraton Affichage Infos

# Scrollbar ***************
style = ttk.Style()
style.theme_use("default")
    #colors

style.configure("Treeview",
                background = "#D3D3D3",
                foreground = "black",
                rowheight = 60,
                fieldbackground = "#D3D3D3",
                font=(True, 32)
                )
#modify
 
#couleur selection
style.map("Treeview", background = [("selected", "#BC9E82")])

Label_equipe = Label(root, text = "EQUIPES ", bg = "#999999", fg = "white")
Label_equipe.place(x = 90, y = 125, width = 150)

Affiche = ttk.Treeview(root, columns=(1), height = 10, show = "headings")
Affiche.place(x = 15, y = 150, width = 300, height = 400 )
Affiche.column(1, anchor=CENTER)
Affiche.heading(1, text = "NOM EQUIPE")

# First Scrollbar
scroll = Scrollbar(Affiche, orient = VERTICAL, command = Affiche.yview)
Affiche.config(yscrollcommand = scroll.set)
scroll.pack(side = RIGHT, fill = Y)

scroll_ = Scrollbar(Affiche, orient = HORIZONTAL, command = Affiche.xview)
Affiche.config(xscrollcommand = scroll_.set)
scroll_.pack(side = BOTTOM, fill = X)


#modify
"""
Affiche2 :
"""
"""
# Add image file
bg = PhotoImage(file = "foot1.png")
  
# Show image using label
label1 = Label( root, image = bg, height=200)
#label1.place(x = 0, y = 0)
label1.grid(row=0, column=3, sticky=NE)
  
label2 = Label( root, text = "Welcome")
#label2.pack(pady = 50)
"""
#Affichage des images
bg = PhotoImage(file = "foot1.png")
label_im = Label(root, image=bg)
m=36
label_im.place(x=635+m, y = 0, width=618-m, height=150)

bg2 = PhotoImage(file = "football_player_PNG80.png")
label_im2 = Label(root, image=bg2)
label_im2.place(x=470, y = 0, width=200, height=150)

#tv1.column(column, anchor=CENTER) # This will center text in rows
#tv1.heading(column, text=column)

Label_result = Label(root, text = "RESULTATS DU TIRAGE ", bg = "#999999", fg = "white")
Label_result.place(x = 785, y = 125, width = 150)

Affiche2 = ttk.Treeview(root, columns=(1,2,3,4), height = 10, show = "headings")
Affiche2.place(x = 470, y = 150, width = 800, height = 400 )
Affiche2.column(1, anchor=CENTER)
Affiche2.heading(1, text = "EQUIPE 1")
Affiche2.column(2, anchor=CENTER)
Affiche2.heading(2, text = "CONTRE")
Affiche2.column(3, anchor=CENTER)
Affiche2.heading(3, text = "EQUIPE 2")
Affiche2.column(4, anchor=CENTER)
Affiche2.heading(4, text = "QUALIFIES")

Affiche2.column(1, width = 200)
Affiche2.column(2, width = 160)
Affiche2.column(3, width = 200)
Affiche2.column(4, width = 200)


#Affiche2.column(1, width = 20)

# 2nd Scrollbar
scroll2 = Scrollbar(Affiche2, orient = VERTICAL, command = Affiche.yview)
Affiche2.config(yscrollcommand = scroll2.set)
scroll2.pack(side = RIGHT, fill = Y)

scroll2_ = Scrollbar(Affiche2, orient = HORIZONTAL, command = Affiche2.xview)
Affiche2.config(xscrollcommand = scroll2_.set)
scroll2_.pack(side = BOTTOM, fill = X)


# Affichage des infos sur L'ecran du 1er treeview
connection = sqlite3.connect("equipes.db")
curseur = connection.cursor()
select = curseur.execute("select Nom_Equipe from EQUIPE")
for ligne in select:
    Affiche.insert("", END, value = ligne)

# ********* Personnalisation de l'affichage ***************

connection.close()


# Affichage des infos sur L'ecran du 2eme treeview

"""
connection = sqlite3.connect("tirage_results.db")
curseur = connection.cursor()
select = curseur.execute("SELECT * FROM TIRAGE")
for record in select:
    Affiche2.insert(parent='', index='end', text="",
                 values=(record[0], record[1], record[2], record[3]))

connection.close()
"""


# anchor with place ????

# Label identifiants

NomEquipe = Label(root , text = "NOM EQUIPE:" ,  bg="#AE5D2D" , fg = "white")
NomEquipe.place(x=15 , y = 50 , width = 100)
entreeEquipe = Entry(root, bd = 4, bg = "white", fg = "black")
entreeEquipe.place(x = 130,  y =50 , width=150)

# Ajout Bouttons

b1 = Button(root, text = "AJOUTER EQUIPE", bg = "#AE5D2D", fg = "white", command = T.Ajout_Equipe)
b1.place(x = 90, y = 90, width = 150)

b2 = Button(root, text = "MELANGER EQUIPE", bg = "#AE5D2D", fg = "white", command=T.melanger)
b2.place(x = 317, y = 250, width = 148)

b3 = Button(root, text = "TIRER EQUIPE", bg = "#AE5D2D", fg = "white", command=T.tirer)
b3.place(x = 317, y = 350, width = 148)

b4 = Button(root, text = "NOUVEAU TIRAGE ", bg = "#AE5D2D", fg = "white", command = T.nouveau_tirage)
b4.place(x = 470, y = 550, width = 150)

b5 = Button(root, text = "Aide/Help (GUIDE) ", bg = "#AE5D2D", fg = "white", command = T.Aide)
b5.place(x = 317, y = 450, width = 150)

b6 = Button(root, text = "Quitter App / Exit", bg = "#AE5D2D", fg = "white", command = T.Quiter )
b6.place(x = 1100, y = 550, width = 150)

b7 = Button(root, text = "SUPPRIMER SELECTION", bg = "#AE5D2D", fg = "white",
            command=T.Supprimer_equipe)
b7.place(x = 15, y = 550, width = 130)

b8 = Button(root, text = "SUPPRIMER TOUT", bg = "#AE5D2D", fg = "white", 
            command=T.Supprimer_tout)
b8.place(x = 170, y = 550, width = 130)


root.mainloop()

#os.system("PAUSE")