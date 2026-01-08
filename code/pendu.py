import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# Charger les mots depuis le fichier
with open("mots.txt", encoding="utf-8") as fichier:
    mots = fichier.read().splitlines()

# Demander le pseudo
root = tk.Tk()
root.withdraw()
pseudo = simpledialog.askstring("Pseudo", "Entrez votre pseudo :") or "Joueur"

class PenduApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu du Pendu")
        self.root.geometry("500x600")

        # Choisir une couleur de fond aléatoire
        self.root.configure(bg=random.choice(["lightblue", "lightyellow", "lightpink", "lightgray", "lightcoral"]))

        # Variables du jeu
        self.mot = random.choice(mots)
        self.lettres = []
        self.faux = 0
        self.score = 0

        # Interface
        self.label_accueil = tk.Label(root, text=f"Bienvenue, {pseudo} !", font=("Arial", 16, "bold"), bg=self.root.cget("bg"))
        self.label_accueil.pack(pady=10)

        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack(pady=10)

        self.label_mot = tk.Label(root, text="_ " * len(self.mot), font=("Arial", 18), bg=self.root.cget("bg"))
        self.label_mot.pack(pady=10)

        self.entry_lettre = tk.Entry(root, font=("Arial", 14), justify="center")
        self.entry_lettre.pack(pady=10)

        self.bouton_valider = tk.Button(root, text="Valider", font=("Arial", 14, "bold"), bg="green", fg="white", width=10, height=2, command=self.verifier_saisie)
        self.bouton_valider.pack(pady=10)

        self.label_lettres = tk.Label(root, text="Lettres utilisées : ", font=("Arial", 12), bg=self.root.cget("bg"))
        self.label_lettres.pack(pady=5)

        self.label_score = tk.Label(root, text="Score : 0", font=("Arial", 12), bg=self.root.cget("bg"))
        self.label_score.pack(pady=5)

        self.dessiner_pendu()
        self.root.protocol("WM_DELETE_WINDOW", self.fermer_application)
        self.entry_lettre.bind("<Return>", self.verifier_saisie)

    def fermer_application(self):
        self.root.quit()  # Quitter proprement la boucle principale Tkinter
        self.root.destroy()  # Détruire la fenêtre Tkinter

    def dessiner_pendu(self):
        self.canvas.delete("all")
        self.canvas.create_line(50, 250, 150, 250)
        self.canvas.create_line(100, 50, 100, 250)
        self.canvas.create_line(100, 50, 200, 50)
        self.canvas.create_line(200, 50, 200, 80)

        if self.faux > 0:
            self.canvas.create_oval(180, 80, 220, 120)
        if self.faux > 1:
            self.canvas.create_line(200, 120, 200, 180)
        if self.faux > 2:
            self.canvas.create_line(200, 130, 170, 160)
        if self.faux > 3:
            self.canvas.create_line(200, 130, 230, 160)
        if self.faux > 4:
            self.canvas.create_line(200, 180, 170, 230)
        if self.faux > 5:
            self.canvas.create_line(200, 180, 230, 230)

    def verifier_saisie(self, event=None):
        saisie = self.entry_lettre.get().strip().lower()
        self.entry_lettre.delete(0, tk.END)

        if not saisie.isalpha():
            messagebox.showwarning("Entrée invalide", "Veuillez entrer uniquement des lettres ou un mot entier.")
            return

        if len(saisie) == 1:
            if saisie in self.lettres:
                messagebox.showwarning("Lettre déjà utilisée", "Vous avez déjà essayé cette lettre.")
                return
            self.lettres.append(saisie)
            if saisie not in self.mot:
                self.faux += 1
            else:
                self.score += 1
        elif len(saisie) == len(self.mot):
            if saisie == self.mot:
                messagebox.showinfo("Victoire", f"Félicitations ! Vous avez trouvé le mot : {self.mot}")
                self.fermer_application()
                return
            else:
                self.faux += 1
                self.lettres.append(saisie)
                messagebox.showwarning("Mauvaise réponse", "Mauvaise réponse ! Vous perdez une tentative.")
        else:
            messagebox.showwarning("Entrée invalide", "Le mot saisi ne correspond pas à la longueur du mot à deviner.")

        self.label_mot.config(text=" ".join([l if l in self.lettres else "_" for l in self.mot]))
        self.label_lettres.config(text="Lettres utilisées : " + " ".join(self.lettres))
        self.label_score.config(text=f"Score : {self.score}")
        self.dessiner_pendu()

        if "_" not in self.label_mot.cget("text"):
            messagebox.showinfo("Victoire", f"Bravo ! Le mot était {self.mot}")
            self.fermer_application()
        elif self.faux > 5:
            messagebox.showinfo("Perdu", f"Dommage, vous avez perdu ! Le mot était {self.mot}")
            self.fermer_application()

root = tk.Tk()
app = PenduApp(root)
root.mainloop()
