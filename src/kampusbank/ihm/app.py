"""Fenêtre principale de l'application KampusBank."""

import tkinter as tk
from tkinter import ttk


class KampusBankApp(tk.Tk):
    """Fenêtre principale de KampusBank."""

    def __init__(self) -> None:
        super().__init__()

        self.title("KampusBank")
        self.geometry("500x400")
        self.resizable(False, False)

        self._creer_interface()

    def _creer_interface(self) -> None:
        """Crée les composants de la fenêtre d'accueil."""

        conteneur = ttk.Frame(self, padding=40)
        conteneur.pack(expand=True, fill="both")

        titre = ttk.Label(
            conteneur,
            text="KampusBank",
            font=("Arial", 26, "bold"),
        )
        titre.pack(pady=(40, 10))

        sous_titre = ttk.Label(
            conteneur,
            text="Votre banque universitaire",
            font=("Arial", 12),
        )
        sous_titre.pack(pady=(0, 40))

        bouton_connexion = ttk.Button(
            conteneur,
            text="Se connecter",
        )
        bouton_connexion.pack(
            pady=10,
            ipadx=30,
            ipady=8,
        )

        bouton_inscription = ttk.Button(
            conteneur,
            text="S'inscrire",
        )
        bouton_inscription.pack(
            pady=10,
            ipadx=40,
            ipady=8,
        )


def lancer_application() -> None:
    """Lance l'application KampusBank."""
    application = KampusBankApp()
    application.mainloop()