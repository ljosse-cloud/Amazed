from map import *
from utils import *
import tkinter as tk


name_to_save = ""
save_the_file=False

def transmitting_file_name_to_game(): #fonction associée à la fenêtre de la sauvegarde
    global the_name
    global name_to_save
    global save_the_file
    name_to_save=the_name.get() #Sauvegarde le nom choisi
    save_the_file=True # Active un code dans le ficher game
    window.destroy()

def save() : # Fonction créant une fenêtre Tkinter sur la sauvegarde
    global name
    global the_name
    global window
    window = tk.Tk()
    window.geometry("200x100")
    the_name=tk.StringVar()

    label = tk.Label(master = window, text = "Sauvegarde")
    label.pack()

    FileName = tk.Entry(master = window, width=30, textvariable=the_name)
    FileName.pack()

    
    save_button= tk.Button(master=window, text="Executer", width=10, command=transmitting_file_name_to_game)
    save_button.pack()
    
    window.mainloop()
    
open_the_file=False
name_to_open=""

def transmit_opening_file_name_to_game(): #Fonction ouvrant les fichiers nommés
    global opening_file_name
    global name_to_open
    global open_the_file
    name_to_open=opening_file_name.get()
    open_the_file=True
    window.destroy()
def open_default_lab(): #Fonction ouvrant le labyrinthe de base
    global name_to_open
    global open_the_file
    name_to_open="test"
    open_the_file=True
    window.destroy()
def open_amazed_lab(): #Fonctino ouvrant le labyrinthe Amazed
    global name_to_open
    global open_the_file
    name_to_open="Amazed"
    open_the_file=True
    window.destroy()
def open() : #Fenetre Tkinter ouvrant les fichiers
    global opening_file_name
    global window
    window = tk.Tk()
    window.geometry("300x200")
        

    FileNameLabel = tk.Label(master = window, text = "Entrez le nom du fichier")
    FileNameLabel.pack()
    
    opening_file_name=tk.StringVar() 
    FileNameEntry = tk.Entry(master = window, textvariable=opening_file_name)
    FileNameEntry.pack()

    default_lab= tk.Button(master=window, text="Labyrinthe par défaut", width=18, command=open_default_lab)
    default_lab.pack()
    default_lab= tk.Button(master=window, text="AMAZING level", width=12, command=open_amazed_lab)
    default_lab.pack()
    open_button= tk.Button(master=window, text="Executer", width=10, command=transmit_opening_file_name_to_game)
    open_button.pack()
    
    window.mainloop()
    
    

