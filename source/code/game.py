

# importation des bibliotheques ainsi que des fonctions definies dans les autres pages de code
from map import *
from utils import *
import window
from time import sleep
import tkinter as tk
import pyxel as px

class Player:
    def __init__(self):
        self.teleportable = True #variable définissant si le joueur peut être téléporté
        self.position = (0, 0) #variable définissant la position du joueur (tuple de coordonnées)
        self.orientation = 0 #peut prendre 4 valeurs

class Camera:
    def __init__(self):
        self.position = (0, 0) #variable définissant la location de départ de la caméra en mode contruction (tuple de coordonnées)
        self.zoom = 4
        self.speed = 1

class Game:
    def __init__(self):
        self.screen = (256, 256) #définit la taille de l'abscisse et de l'ordonnée de l'écran par un tuple
        px.init(self.screen[0], self.screen[1], title = "Amaze'd", fps = 24, quit_key = px.KEY_NONE) # le programme se jouera 24 fois par seconde
        px.load("../ressources/images.pyxres") # importe la banque d'image et de sons

        # initialisation des variables
        self.mode = 3 # commence le jeu sur le mode menu

        self.player = Player()
        self.camera = Camera()

        self.map = load_map_file("../maps/test.map") # télécharge la map par défaut

        self.installing_portal = False
        self.help_menu = False
        self.return_b = 0
        self.play_music = True
        self.anim = 0
        self.wait=False
        self.help_text = ""
        with open("../ressources/texte aide.txt", "r") as file:
            self.help_text += file.read() #chargement du texte d'aide écrit dans un fichier txt

        self.path = []
        self.path_showed=False

        self.portal_entry = Portal((0, 0), 1, 0)
        self.portal_count = 0



        # démarrage du programme qui tourne en boucle 
        px.run(self.update, self.render)

    def update(self):
        match self.mode:
            case 0: # cas de l'edition
                px.stop()

                if window.save_the_file==True:
                    window.save_the_file=False
                    save_map(self.map, ("../maps/"+window.name_to_save+".map"))
                if window.open_the_file == True:
                    window.open_the_file = False
                    self.map.tiles = []
                    self.map = load_map_file("../maps/"+window.name_to_open+".map")
                    self.portal_count=update_portal_count(self.map)
                self.camera.zoom += px.mouse_wheel # modifie le zoom
                # empêche le zoom de prendre des valeurs extrêmes
                if self.camera.zoom < 1:
                    self.camera.zoom = 1
                elif self.camera.zoom > 24:
                    self.camera.zoom = 24

                # position de la case où la souris est posée
                mouse = ((px.mouse_x-px.mouse_x%self.camera.zoom)//self.camera.zoom+self.camera.position[0], (px.mouse_y-px.mouse_y%self.camera.zoom)//self.camera.zoom+self.camera.position[1])

                # si la musique est activée, la jouer
                if (self.play_music == True):
                    px.playm(0, True, True)

                # pose un bloc s'il n'y a rien
                if px.btn(px.MOUSE_BUTTON_LEFT) and (not self.map.has(mouse)) and (self.wait == True):
                    if px.btn(px.KEY_CTRL):
                        self.map.start.position = mouse
                    else:
                        self.map.tiles.append(Tile(mouse, 0))

                # efface un bloc ou déplace l'arrivée (en fonction de si la touche CTRL est pressée)
                if px.btn(px.MOUSE_BUTTON_RIGHT):
                    if px.btn(px.KEY_CTRL) and (not self.map.has(mouse)):
                        self.map.end.position = mouse
                    elif not px.btn(px.KEY_CTRL):
                        self.map.remove(mouse)

                # sauvegarde la map dans un fichier
                if px.btn(px.KEY_CTRL) and px.btnp(px.KEY_S):
                    window.save()

                # pose un portail
                if px.btnp(px.KEY_P) and not(self.map.has(mouse)):
                    if self.installing_portal: # si on a déjà posé un premier portail
                        self.map.tiles += [self.portal_entry, Portal(mouse, 1, self.portal_count)]
                        self.portal_count += 1
                        self.installing_portal = False
                    else: # si on pose le premier portail du couple
                        self.installing_portal = True
                        self.portal_entry = Portal(mouse, 1, self.portal_count)
                
                # charge le chemin le plus court si le labyrinthe est résolvable
                if px.btnp(px.KEY_S) and px.btn(px.KEY_SHIFT):
                    px.stop()
                    self.path = find_path(self.map, self.map.start.position[0], self.map.start.position[1], self.map.end.position[0], self.map.end.position[1])
                    self.path_showed=True


                # deplacements de la caméra
                if px.btn(px.KEY_RIGHT):
                    self.camera.position = right(self.camera.position, self.camera.speed)
                elif px.btn(px.KEY_LEFT):
                    self.camera.position = left(self.camera.position, self.camera.speed)
                elif px.btn(px.KEY_DOWN):
                    self.camera.position = down(self.camera.position, self.camera.speed)
                elif px.btn(px.KEY_UP):
                    self.camera.position = up(self.camera.position, self.camera.speed)
                
                # passe en mode jeu si la touche espace est pressée
                if px.btnp(px.KEY_SPACE):
                    self.mode = 1
                    self.player.position = self.map.start.position
                    self.player.orientation = 0
                
                # contrôles pour revenir sur le menu principal
                if px.btnp(px.KEY_ESCAPE) or (10 < px.mouse_x < 26 and 230 < px.mouse_y < 246 and px.btn(px.MOUSE_BUTTON_LEFT) == True):
                    self.mode = 2
                if px.btnp(px.KEY_SPACE):
                    # si la musique est activée, la jouer 
                    if (self.play_music == True):
                        px.playm(0, True, True)
                
            case 1: # cas du mode jeu
                right_tile = lambda : self.map.get_tile(right(self.player.position))
                left_tile = lambda : self.map.get_tile(left(self.player.position))
                down_tile = lambda : self.map.get_tile(down(self.player.position))
                up_tile = lambda : self.map.get_tile(up(self.player.position))

                # déplacement du joueur en changeant son orientation et en le rendant téléportable
                if px.btnp(px.KEY_RIGHT, 8, 2) and not(right_tile() != None and right_tile().id == 0):
                    self.player.position = right(self.player.position)
                    self.player.orientation = 3
                    self.player.teleportable = True
                if px.btnp(px.KEY_LEFT, 8, 2) and not(left_tile() != None and left_tile().id == 0):
                    self.player.position = left(self.player.position)
                    self.player.orientation = 2
                    self.player.teleportable = True
                if px.btnp(px.KEY_DOWN, 8, 2) and not(down_tile() != None and down_tile().id == 0):
                    self.player.position = down(self.player.position)
                    self.player.orientation = 0
                    self.player.teleportable = True
                if px.btnp(px.KEY_UP, 8, 2) and not(up_tile() != None and up_tile().id == 0):
                    self.player.position = up(self.player.position)
                    self.player.orientation = 1
                    self.player.teleportable = True

                # téléporte le joueur s'il est présent sur un portail
                if self.player.teleportable:
                    for p in self.map.tiles:
                        if type(p) is Portal and self.player.position == p.position and self.player.teleportable:
                            for exit in self.map.tiles:
                                if type(exit) is Portal and p.position != exit.position and p.portal_id == exit.portal_id:
                                    self.player.position = exit.position
                                    self.player.teleportable = False
                                    break

                # félicite le joueur lorsqu'il arrive sur la case d'arrivée
                if self.player.position == self.map.end.position:
                    self.mode = 5   

                # passe en mode édition si la touche espace est pressée
                if px.btnp(px.KEY_SPACE):
                    self.mode = 0

                # revient sur le menu principal si la touche échap est pressée
                if px.btnp(px.KEY_ESCAPE) or (10 < px.mouse_x < 26 and 230 < px.mouse_y < 246 and px.btn(px.MOUSE_BUTTON_LEFT) == True):
                    self.mode = 2   
                    
            case 2: # cas du menu
                px.stop()

                self.return_b = 0
                # sauvegarde/ouverture
                if window.save_the_file==True:
                    window.save_the_file=False
                    save_map(self.map, ("../maps/"+window.name_to_save+".map"))
                if window.open_the_file == True:
                    window.open_the_file = False
                    self.map.tiles = []
                    self.map = load_map_file("../maps/"+window.name_to_open+".map")
                    self.portal_count=update_portal_count(self.map)

                # bouton aide
                if 220 < px.mouse_x < 256 and 5 < px.mouse_y < 21 and px.btn(px.MOUSE_BUTTON_LEFT) == True: 
                    self.mode = 4
                
                # bouton retour au jeu
                if 175 < px.mouse_x < 251 and 220 < px.mouse_y < 244:
                    self.return_b = 1
                    if px.btn(px.MOUSE_BUTTON_LEFT) == True:
                        self.mode = 0
                        sleep(0.0000001)
                        self.wait = True
                        
                # bouton nouveau
                if 10 < px.mouse_x < 138 and 50 < px.mouse_y < 74 and px.btn(px.MOUSE_BUTTON_LEFT) == True:
                    self.map.tiles = []
                    sleep(0.0000001)
                    self.wait == True
                    self.path=[]
                    self.map.start.position=(0,0)
                    self.map.end.position=(0,1)
                    self.mode = 0
                    
                # bouton ouvrir
                if 10 < px.mouse_x < 138 and 100 < px.mouse_y < 124 and px.btn(px.MOUSE_BUTTON_LEFT) == True:
                    window.open()
                    self.path.clear()

                    self.mode = 0
                    
                # bouton sauvegarder
                if 10 < px.mouse_x < 138 and 150 < px.mouse_y < 174 and px.btn(px.MOUSE_BUTTON_LEFT) == True:
                    window.save()
                    self.mode = 0

                # bouton musique
                if (232 < px.mouse_x < 248 and 32 < px.mouse_y < 48 and px.btnp(px.MOUSE_BUTTON_LEFT)) == True:
                    self.play_music = not self.play_music
                    
            case 3: # écran titre
                if px.btnp(px.KEY_SPACE):
                    self.mode = 2
            case 4: # écran d'aide
                # bouton retour menu
                if 230 < px.mouse_x < 246 and 195 < px.mouse_y < 211 and px.btnp(px.MOUSE_BUTTON_LEFT) == True:
                    self.mode = 2

                # bouton retour à l'édition
                if 175 < px.mouse_x < 251 and 220 < px.mouse_y < 244:
                    self.return_b = 1
                    if px.btn(px.MOUSE_BUTTON_LEFT) == True:
                        self.mode = 0
                else :
                    self.return_b = 0
            case 5: # écran de réussite
                # fait progresser l'animation toutes les 5 frames
                if px.frame_count%10 >= 5:
                    self.anim = 0
                else:
                    self.anim = 1
                        
                # retourne sur le mode édition après avoir pressé la barre espace
                if px.btnp(px.KEY_SPACE):
                    self.mode = 0
                

    def render(self):
        # vide l'écran
        px.cls(0)

        # position de la case où est placée la souris
        mouse = ((px.mouse_x-px.mouse_x%self.camera.zoom)//self.camera.zoom+self.camera.position[0], (px.mouse_y-px.mouse_y%self.camera.zoom)//self.camera.zoom+self.camera.position[1])

        if self.mode <= 1:
            for t in self.map.tiles+[self.map.start, self.map.end]:
                color = 0
                match t.id:
                    case -2: # cas de la case depart
                        color = 5
                    case -1: # cas de la case d'arrivée
                        color = 8
                    case 0: # cas des murs
                        color = 11
                    case 1:
                        color = 7 # cas des portails
                    # rajouter un cas pour les portails. Plus generalement s'occuper des portails

                POV = (0, 0)
                if self.mode == 1:
                    POV = self.player.position
                    # affiche la texture de la tuile
                    if t.id < 0:
                        px.blt(8*(t.position[0]-POV[0])+self.screen[0]//2, 8*(t.position[1]-POV[1])+self.screen[1]//2, 0, 40 + (-t.id-1)*8, 0, 8, 8, 0)
                    elif t.id == 0:
                        px.blt(8*(t.position[0]-POV[0])+self.screen[0]//2, 8*(t.position[1]-POV[1])+self.screen[1]//2, 0, 32, 0, 8, 8, 0)
                    elif t.id == 1:
                        px.blt(8*(t.position[0]-POV[0])+self.screen[0]//2, 8*(t.position[1]-POV[1])+self.screen[1]//2, 0, 96,144,8,8,0)
                elif self.mode == 0:
                    POV = self.camera.position
                    # affiche la couleur de la tuile
                    px.rect(self.camera.zoom*(t.position[0]-POV[0]), self.camera.zoom*(t.position[1]-POV[1]), self.camera.zoom, self.camera.zoom, color)

                    # relie les portails par une ligne si la souris est sur l'un des deux
                    if type(t) is Portal and mouse == t.position:
                        for exit in self.map.tiles:
                            if type(exit) is Portal and exit.position != t.position and t.portal_id == exit.portal_id: # trouve le portail correspondant
                                px.line(self.camera.zoom*(t.position[0]-POV[0]), self.camera.zoom*(t.position[1]-POV[1]), self.camera.zoom*(exit.position[0]-POV[0]), self.camera.zoom*(exit.position[1]-POV[1]), 7)

            mode_str = ""
            if self.mode == 1:
                mode_str = "mode : play"
                center = (self.screen[0]//2, self.screen[1]//2)
                px.blt(center[0]-center[0]%8, center[1]-center[1]%8, 0, 8*self.player.orientation, 0, 8, 8, 0) # affiche le joueur en fonction de son orientation
            elif self.mode == 0:
                mode_str = "mode : edit"
                # affiche une case grise à la positon de la souris
                px.rect(px.mouse_x-px.mouse_x%self.camera.zoom, px.mouse_y-px.mouse_y%self.camera.zoom, self.camera.zoom, self.camera.zoom, 13)

                # affiche le chemin de résolution
                for t in self.path:
                    px.rect(self.camera.zoom*(t[0]-POV[0]), self.camera.zoom*(t[1]-POV[1]), self.camera.zoom, self.camera.zoom, 12)
                if self.path_showed == True and px.btnp(px.KEY_E):
                    self.path=[]
                    self.path_sowed=False
            px.text(self.screen[0]-4*len(mode_str), 0, mode_str, 7) # affiche le mode si on est en mode jeu ou en mode édition
            px.blt(10, 230, 0, 96, 128, 16, 16, 0) # bouton menu
            
        elif self.mode == 3: # affichage de l'écran titre
            px.blt(30, 100, 0, 0, 160, 194, 46, 0)
            px.text(128, 158, "Appuyer sur Espace_", 6)
            px.text(164, 245, "|AEE KP OD PR UN|", 6)

        elif self.mode == 5: # affichage de l'écran de réussite
            px.cls(6)
            px.rectb(100, 90, 56, 20, 0)
            px.text(108, 98, "B R A V O !", 0)
            px.blt(119, 120, 0, 159, 0 + self.anim*32, 18, 32, 9)
            px.text(164, 235, "Appuyez sur Espace_", 0)
            
        else: # affichage du menu principal et de l'aide
            px.rect(0, 0, 256, 25, 13) # bandeau de l'aide
            px.blt(10, 2, 0, 56, 0, 95, 24, 0) # nom du jeu
            px.blt(175, 220, 0, 16, 104+self.return_b*26, 73, 26, 0) # bouton retour

            if self.mode == 2: # menu principal
                for i in range (3):
                    px.blt(10, 50*(i+1), 0, 0, 24+(i*24), 128, 24, 0) # boutons nouveau, ouvrir et sauvegarder
            
                px.blt(220, 4, 0, 0, 8, 32, 16, 0) # bouton aide
                if self.play_music == True:
                    px.blt(232, 32, 0, 0, 120, 16, 16, 0)
                elif self.play_music == False:
                    px.blt(232, 32, 0, 0, 136, 16, 16, 0)
                
            if self.mode == 4: # écran d'aide
                px.blt(230, 195, 0, 96, 128, 16, 16, 0) # bouton menu
                px.text(20, 35, self.help_text, 7) # texte de l'aide
            
            px.blt(px.mouse_x, px.mouse_y, 0, 0, 106, 16, 14, 0) # curseur, a la fin pour etre au dessus des autres elements

