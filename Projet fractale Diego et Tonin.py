# Projet NSI - Terminale
# Auteurs : Diego et Tonin
# Titre : Affichage de courbes fractales interactives

import tkinter as tk
from tkinter import colorchooser
import math

# Variables globales
couleur = "#FF0000"           # Couleur par défaut des dessins
triangles = []                # Liste de triangles pour le Sierpinski
segments_koch = []            # Liste de segments pour le flocon de Koch
branches = []                 # Liste de branches pour l’arbre fractal
epaisseur = 1                 # Épaisseur du trait
vitesse = 10                  # Vitesse d’animation
choix_dessin = "Triangle de Sierpinski"  # Dessin sélectionné par défaut


# FONCTIONS D'INTERACTION ET DE PARAMÉTRAGE

def changer_couleur(event=None):
    """Ouvre une boîte de dialogue pour choisir une nouvelle couleur et
    met à jour la couleur du cercle affiché sur le canevas."""
    global couleur
    nouvelle_couleur = colorchooser.askcolor(title="Choisis une couleur")[1]
    if nouvelle_couleur:
        couleur = nouvelle_couleur
        canvas.itemconfig(cercle, fill=couleur)


def set_epaisseur(val):

    global epaisseur
    epaisseur = int(val)


def set_vitesse(val):

    global vitesse
    vitesse = int(val)


def set_choix(val):

    global choix_dessin
    choix_dessin = val


# --- FONCTIONS DU TRIANGLE DE SIERPINSKI ---

def creer_triangles(x1, y1, x2, y2, x3, y3, niveau):

    if niveau == 0:
        triangles.append((x1, y1, x2, y2, x3, y3))
    else:
        # Calcul des milieux des côtés
        mx12 = (x1 + x2) / 2
        my12 = (y1 + y2) / 2
        mx23 = (x2 + x3) / 2
        my23 = (y2 + y3) / 2
        mx31 = (x3 + x1) / 2
        my31 = (y3 + y1) / 2


        creer_triangles(x1, y1, mx12, my12, mx31, my31, niveau - 1)
        creer_triangles(x2, y2, mx23, my23, mx12, my12, niveau - 1)
        creer_triangles(x3, y3, mx31, my31, mx23, my23, niveau - 1)


def dessiner():

    if triangles:
        x1, y1, x2, y2, x3, y3 = triangles.pop(0)
        canvas.create_polygon(x1, y1, x2, y2, x3, y3,
                              fill=couleur, outline="black", width=epaisseur)
        canvas.after(vitesse, dessiner)


# --- FONCTIONS DU FLOCON DE KOCH ---

def dessiner_koch(x1, y1, x2, y2, niveau):

    if niveau == 0:
        segments_koch.append((x1, y1, x2, y2))
    else:
        dx = (x2 - x1) / 3
        dy = (y2 - y1) / 3


        xA, yA = x1, y1
        xB, yB = x1 + dx, y1 + dy
        xD, yD = x1 + 2 * dx, y1 + 2 * dy
        xE, yE = x2, y2


        angle = math.radians(60)
        xC = xB + math.cos(angle) * dx - math.sin(angle) * dy
        yC = yB + math.sin(angle) * dx + math.cos(angle) * dy


        dessiner_koch(xA, yA, xB, yB, niveau - 1)
        dessiner_koch(xB, yB, xC, yC, niveau - 1)
        dessiner_koch(xC, yC, xD, yD, niveau - 1)
        dessiner_koch(xD, yD, xE, yE, niveau - 1)


def dessiner_segments_koch():

    if segments_koch:
        x1, y1, x2, y2 = segments_koch.pop(0)
        canvas.create_line(x1, y1, x2, y2, fill=couleur, width=epaisseur)
        canvas.after(vitesse, dessiner_segments_koch)

# FONCTION DU FLOCON DE KOCH
def dessiner_flocon_koch():
    global segments_koch
    segments_koch = []

    largeur = canvas.winfo_width()
    hauteur = canvas.winfo_height()
    taille = min(largeur, hauteur) / 3
    cx, cy = largeur / 2, hauteur / 2

    x1 = cx
    y1 = cy - taille / math.sqrt(3)
    x2 = cx - taille / 2
    y2 = cy + taille / (2 * math.sqrt(3))
    x3 = cx + taille / 2
    y3 = y2


    dessiner_koch(x1, y1, x2, y2, 4)
    dessiner_koch(x2, y2, x3, y3, 4)
    dessiner_koch(x3, y3, x1, y1, 4)

    # Dessin progressif
    dessiner_segments_koch()


# FONCTIONS DE L'ARBRE FRACTAL

def creer_arbre(x1, y1, angle, longueur, niveau):
    """Crée récursivement les branches d’un arbre fractal."""
    if niveau == 0:
        return
    x2 = x1 + math.cos(angle) * longueur
    y2 = y1 - math.sin(angle) * longueur
    branches.append((x1, y1, x2, y2))


    creer_arbre(x2, y2, angle + math.pi / 6, longueur * 0.7, niveau - 1)
    creer_arbre(x2, y2, angle - math.pi / 6, longueur * 0.7, niveau - 1)


def dessiner_branches():
    """Dessine progressivement les branches stockées dans la liste."""
    if branches:
        x1, y1, x2, y2 = branches.pop(0)
        canvas.create_line(x1, y1, x2, y2, fill=couleur, width=epaisseur)
        canvas.after(vitesse, dessiner_branches)


def dessiner_arbre():
    """Initialise et trace un arbre fractal centré en bas du canevas."""
    global branches
    branches = []
    largeur = canvas.winfo_width()
    hauteur = canvas.winfo_height()
    x0, y0 = largeur / 2, hauteur - 50
    creer_arbre(x0, y0, math.pi / 2, hauteur / 4, 9)
    dessiner_branches()


# DESSIN PRINCIPAL SELON LE CHOIX DE L’UTILISATEUR

def dessiner_figure():
    """Efface le canevas et dessine la fractale choisie."""
    canvas.delete("all")
    global cercle, triangles
    triangles.clear()

    # Cercle cliquable pour choisir la couleur
    cercle = canvas.create_oval(10, 10, 90, 90, fill=couleur, outline="black")
    canvas.tag_bind(cercle, "<Button-1>", changer_couleur)

    largeur = canvas.winfo_width()
    hauteur = canvas.winfo_height()
    if largeur < 200 or hauteur < 200:
        largeur, hauteur = 800, 600

    # Sélection du dessin selon le menu
    if choix_dessin == "Triangle de Sierpinski":
        x1, y1 = largeur // 2, 50
        x2, y2 = 50, hauteur - 50
        x3, y3 = largeur - 50, hauteur - 50
        creer_triangles(x1, y1, x2, y2, x3, y3, 6)
        dessiner()
    elif choix_dessin == "Flocon de Koch":
        dessiner_flocon_koch()
    elif choix_dessin == "Arbre fractal":
        dessiner_arbre()


# INTERFACE GRAPHIQUE

def interface():
    """Crée la fenêtre principale Tkinter avec les menus et le canevas."""
    global canvas, cercle, epaisseur_menu, vitesse_scale, choix_menu
    fenetre = tk.Tk()
    fenetre.title("Fractales interactives")
    fenetre.state("zoomed")


    canvas = tk.Canvas(fenetre, bg="white")
    canvas.pack(fill="both", expand=True)

    # Cercle cliquable pour choisir la couleur
    cercle = canvas.create_oval(10, 10, 90, 90, fill=couleur, outline="black")
    canvas.tag_bind(cercle, "<Button-1>", changer_couleur)

    # Bouton pour lancer le dessin
    bouton = tk.Button(fenetre, text="Dessiner", command=dessiner_figure)
    bouton.place(x=120, y=30)

    # Menu pour l'épaisseur des traits
    tk.Label(fenetre, text="Épaisseur du trait:").place(x=220, y=10)
    epaisseur_menu = tk.IntVar(value=1)
    menu = tk.OptionMenu(fenetre, epaisseur_menu, *range(1, 11),
                         command=lambda val: set_epaisseur(val))
    menu.place(x=220, y=30)

    # Curseur pour la vitesse du dessin
    tk.Label(fenetre, text="Vitesse du dessin:").place(x=360, y=10)
    vitesse_scale = tk.Scale(fenetre, from_=1, to=100, orient="horizontal",
                             command=lambda val: set_vitesse(val))
    vitesse_scale.set(vitesse)
    vitesse_scale.place(x=360, y=30)

    # Menu pour le choix du type de fractale
    tk.Label(fenetre, text="Choix du dessin:").place(x=540, y=10)
    choix_var = tk.StringVar(value=choix_dessin)
    choix_menu = tk.OptionMenu(fenetre, choix_var,
                               "Triangle de Sierpinski", "Flocon de Koch", "Arbre fractal",
                               command=lambda val: set_choix(val))
    choix_menu.place(x=540, y=30)


    fenetre.mainloop()


#LANCEMENT DU PROGRAMME
interface()